# Epicurean AI: Restaurant Discovery

An AI-powered restaurant recommendation engine that leverages LLaMA-3 (via Groq) to curate personalized dining experiences from a massive dataset.

## Features

- 🔍 Filter by location, budget, cuisine, and rating
- 🤖 AI-generated explanations for each recommendation
- ⚡️ Ultra-fast inference via Groq API
- 🎨 Modern dark-theme UI with glassmorphism design

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML + CSS + Vanilla JS |
| Backend | Python 3.11+ / FastAPI |
| Data | Pandas + HuggingFace Datasets |
| LLM | Groq API (LLaMA 3.3 70B) |

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/VGdotcom/Zomato-Project.git
cd Zomato-Project
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 5. Run the server
```bash
uvicorn src.api.main:app --reload
```

### 6. Open the frontend
Open `frontend/index.html` in your browser, or visit `http://localhost:8000/docs` for the Swagger API docs.

## Project Structure

```text
Zomato-Project/
├── src/
│   ├── models/          # Pydantic schemas
│   ├── services/        # Data loader, filter, LLM client
│   ├── utils/           # Preprocessing utilities
│   ├── api/main.py      # FastAPI entrypoint
│   └── config.py        # Environment config
├── frontend/
│   ├── index.html       # Main UI
│   ├── styles.css       # Styling
│   └── app.js           # Frontend logic
├── requirements.txt     # Python dependencies
├── Dockerfile           # Deployment container config
├── .env.example         # API key template
└── README.md
```
