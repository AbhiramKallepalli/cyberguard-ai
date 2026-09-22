# Scenario 2 — Known Attack Patterns

**Input:** 50 records labeled as attacks (not "normal") in NSL-KDD, extracted from KDDTest+.txt, uploaded as scenario2_attacks.csv

**Expected (per spec):** Suspicious events flagged with HIGH risk, correct SHAP factors identified.

**Actual:** 39 out of 50 records (78%) flagged as HIGH risk. SHAP top factors identified meaningful features (e.g. "unusually large amount of data received," "unusually large amount of data sent," "multiple compromised conditions detected") consistent with attack-like behavior.

**Result:** PASS — matches expected outcome. Model correctly flags the majority of true attack records as high risk, with explainable, relevant contributing factors.

**Bonus finding:** LLM Q&A also verified working end-to-end here — asked a question on a flagged event, response was grounded in the actual risk level, anomaly score, and top factors, and recommended disconnecting the device. This also partially covers Scenario 5's requirement.