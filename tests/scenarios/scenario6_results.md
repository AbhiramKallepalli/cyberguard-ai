# Scenario 6 — Empty CSV File

**Input:** A completely empty file (scenario6_empty.csv), uploaded as-is.

**Expected (per spec):** System handles gracefully with a clear message, no crash.

**Actual:** App displayed "File could not be parsed as a CSV." No scan was created, app remained on the upload page for a retry, no crash occurred.

**Result:** PASS — matches expected outcome. Note: the empty file was caught at the CSV-parsing step (before the empty-DataFrame check), since a fully empty file has no readable structure — same safe, graceful outcome either way.