# Scenario 4 — Invalid CSV Schema

**Input:** A 2-column CSV (scenario4_invalid.csv) with only 2 rows, far short of the required 41 NSL-KDD columns.

**Expected (per spec):** System rejects file with clear error message, no partial processing.

**Actual:** App displayed "Invalid format. Expected 41-43 columns (NSL-KDD), got 2." No scan was created, no partial data was processed, app remained on the upload page for a retry.

**Result:** PASS — matches expected outcome exactly.