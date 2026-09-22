# CyberGuard AI
AI-Powered Home Network Security Monitor for IoT Devices

## Project Status
- ✅ V1 Core Features - Complete (Weeks 1-7)
- ✅ Week 8 - CSS + JavaScript Polish (Complete)
- ✅ Week 9 - Testing + Bug Fixes (Complete)
- ✅ Week 10 - Final Report + Submission (Complete)

**Project complete and submitted — September 2026.**

## What This Project Does
Detects unusual activity on home networks using an unsupervised
Isolation Forest model, explains findings in plain English using SHAP,
and provides a local LLM assistant (Phi-3 Mini via Ollama) to help
non-technical homeowners decide what action to take.

## V1 Features - All Complete
- ✅ User login and signup
- ✅ CSV network log upload with validation
- ✅ Isolation Forest anomaly detection (NSL-KDD, 125,973 records)
- ✅ Results page with color-coded risk badges (LOW/MEDIUM/HIGH)
- ✅ LLM Q&A explanation per flagged event (grounded in SHAP factors)
- ✅ SQL database (users, scans, flagged events, LLM responses)

## Testing Summary (Week 9)
- ✅ 16 automated pytest tests, all passing (model, preprocessing, database)
- ✅ All 6 specification test scenarios executed and documented in `/tests/scenarios`
  - Scenario 1 (normal traffic): documented limitation — see final report Section 6
  - Scenario 2 (known attacks): PASS
  - Scenario 3 (unauthenticated access): PASS
  - Scenario 4 (invalid CSV schema): PASS
  - Scenario 5 (LLM Q&A grounding): PASS
  - Scenario 6 (empty CSV): PASS
- ✅ LLM response quality: 2.8 / 3.0 average across 5 evaluated responses — see `/docs/llm_evaluation.md`
- ✅ Bug found and fixed during final review: risk category thresholds were miscalibrated against the model's actual score range, causing 100% of events to classify as HIGH risk. Recalibrated using percentile-based thresholds from the real score distribution — see final report Section 4 for full details.

## Tech Stack
| Component | Technology |
|---|---|
| Backend | Flask |
| Database | SQLite + SQLAlchemy |
| ML Model | Isolation Forest |
| Explainability | SHAP |
| Local LLM | Ollama + Phi-3 Mini |
| Styling | Custom CSS |
| Interactivity | JavaScript + Chart.js |
| Dataset | NSL-KDD (125,973 records) |
| Testing | pytest |

## 10-Week Implementation Progress
| Week | Focus | Status |
|---|---|---|
| Week 1 | Planning + Specification | ✅ Complete |
| Week 2 | Flask Foundation | ✅ Complete |
| Week 3 | File Upload + Preprocessing | ✅ Complete |
| Week 4 | ML Model Training | ✅ Complete |
| Week 5 | SHAP + Plain English Layer | ✅ Complete |
| Week 6 | Results Page + Database | ✅ Complete |
| Week 7 | LLM Q&A Integration | ✅ Complete |
| Week 8 | CSS + JavaScript Polish | ✅ Complete |
| Week 9 | Testing + Bug Fixes | ✅ Complete |
| Week 10 | Final Report + Submission | ✅ Complete |

## How to Run
```bash
# Install dependencies
pip install -r requirements.txt

# Start Ollama (in a separate terminal)
ollama serve

# Run the app
python app.py
```

Then visit `http://127.0.0.1:5000` and log in (or sign up for a new account).

## Documentation
- Full project specification: `/docs`
- Final report (business problem, architecture, evaluation, limitations): `/docs/final_report.md` (also available as `.docx` and `.pdf`)
- LLM evaluation: `/docs/llm_evaluation.md`
- Test scenario results: `/tests/scenarios`

## Dataset
NSL-KDD Network Intrusion Detection Dataset stored in `/data`