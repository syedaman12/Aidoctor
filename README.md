# AI Doctor Chatbot (Demo)

Educational guidance only. Not a diagnosis. For emergencies, call local emergency services.

## Quick Start
```bash
# 1) Create and activate a virtual environment (Windows PowerShell)
python -m venv .venv
. .venv/Scripts/Activate.ps1

# 2) Install deps
pip install -r requirements.txt

# 3) Configure keys
copy .env.example .env
# edit .env and put your OpenAI API key

# 4) Run
python app.py

# 5) Open
http://localhost:5000
