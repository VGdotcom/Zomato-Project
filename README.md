# Zomato AI Restaurant Recommender

An AI-powered application that leverages the Llama-3 model via Groq to recommend the best restaurants from a Zomato dataset based on user preferences.

## Setup

1. Install dependencies:
```bash
pip install -r Docs/requirements.txt
```

2. Set your Groq API key:
```bash
export GROQ_API_KEY="your-api-key"
```

## Running the Application

### CLI Mode
```bash
python src/ui/cli.py
```

### Streamlit Dashboard
```bash
streamlit run src/ui/streamlit_app.py
```

## Testing
```bash
pytest tests/
```
