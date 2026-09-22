# Scenario 1 — Normal Traffic File

**Input:** 50 records labeled "normal" in NSL-KDD, extracted from KDDTest+.txt, uploaded as scenario1_normal.csv

**Expected (per spec):** No events flagged; dashboard shows all green.

**Actual:** All 50 records (100%) were flagged as HIGH risk.

**Result:** FAIL — does not match expected outcome.

**Analysis:** The Isolation Forest model is unsupervised and does not use NSL-KDD's normal/attack labels during training. It flags statistical outliers relative to the training distribution, not "attacks" specifically. This sample of "normal" records may differ enough from the bulk of training data (which includes both normal and attack traffic) to be flagged as anomalous. This suggests the risk score thresholds may need retuning, or that a larger/more representative normal sample would better validate this scenario.

**Action taken:** Documented as a known limitation rather than forcing a false pass. To be discussed in the final report's Limitations section.