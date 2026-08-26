# CyberGuard AI
AI-Powered Home Network Security Monitor for IoT Devices

## Project Status
- ✅ V1 Core Features — Complete (Weeks 1-7)
- 🔄 Week 8 — CSS + JavaScript Polish (In Progress)
- ⏳ Week 9 — Testing (Upcoming)
- ⏳ Week 10 — Final Report + Submission (Upcoming)

## What This Project Does
Detects unusual activity on home networks using an unsupervised 
Isolation Forest model, explains findings in plain English using SHAP, 
and provides a local LLM assistant (Phi-3 Mini via Ollama) to help 
non-technical homeowners decide what action to take.

## V1 Features — All Complete
- ✅ User login and signup
- ✅ CSV network log upload with validation
- ✅ Isolation Forest anomaly detection (NSL-KDD, 125,973 records)
- ✅ Results page with color-coded risk badges (LOW/MEDIUM/HIGH)
- ✅ LLM Q&A explanation per flagged event (grounded in SHAP factors)
- ✅ SQL database (users, scans, flagged events, LLM responses)

## Tech Stack
| Component | Technology |
|---|---|
| Backend | Flask |
| Database | SQLite + SQLAlchemy |
| ML Model | Isolation Forest |
| Explainability | SHAP |
| Local LLM | Ollama + Phi-3 Mini |
| Styling | Custom CSS |
| Interactivity | JavaScript |
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
| Week 8 | CSS + JavaScript Polish | 🔄 In Progress |
| Week 9 | Testing + Bug Fixes | ⏳ Upcoming |
| Week 10 | Final Report + Submission | ⏳ Upcoming |

## How to Run
```bash
# Install dependencies
pip install -r requirements.txt

# Start Ollama (in a separate terminal)
ollama serve

# Run the app
python app.py
```

## Documentation
Full project specification available in `/docs`

## Dataset
NSL-KDD Network Intrusion Detection Dataset stored in `/data`
