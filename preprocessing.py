import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

KDD_COLUMNS = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",
    "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login",
    "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate",
    "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
    "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate"
]

CATEGORICAL_COLUMNS = ["protocol_type", "service", "flag"]


def validate_and_preprocess(file_stream, filename):
    """
    Reads CSV from memory, validates KDD structure,
    cleans and encodes data. Returns processed DataFrame
    or raises ValueError with a clear message.
    """

    # Step 1 — Read CSV into memory
    try:
        df = pd.read_csv(file_stream, header=None)
    except Exception:
        raise ValueError("File could not be parsed as a CSV.")

    # Step 2 — Check not empty
    if df.empty:
        raise ValueError("The uploaded file is empty.")

    # Step 3 — Check row count
    if len(df) > 500000:
        raise ValueError("File too large. Maximum 500,000 rows allowed.")

    # Step 4 — Check column count matches NSL-KDD format
    if df.shape[1] not in (41, 42, 43):
        raise ValueError(
            f"Invalid format. Expected 41-43 columns (NSL-KDD), got {df.shape[1]}."
        )

    # Step 5 — Keep only the 41 feature columns, drop label/difficulty if present
    df = df.iloc[:, :41]
    df.columns = KDD_COLUMNS

    # Step 6 — Handle missing values
    df.fillna(0, inplace=True)

    # Step 7 — Encode categorical columns (protocol_type, service, flag)
    encoders = {}
    for col in CATEGORICAL_COLUMNS:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    # Step 8 — Scale numeric columns
    numeric_columns = [c for c in KDD_COLUMNS if c not in CATEGORICAL_COLUMNS]
    scaler = StandardScaler()
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    return df, len(df)