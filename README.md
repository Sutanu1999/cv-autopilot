# cv-autopilot

AI-powered bot that matches your CV to relevant job postings, optimizes it for ATS, and auto-applies.

## Tech Stack
- Python, Streamlit, Groq API, sentence-transformers, Playwright

## Setup
1. Clone the repo
2. Create a virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Add your API keys to `.env`
6. Run: `streamlit run src/main.py`

## Changelog

### v0.1 — CV Parser
- Added `src/parser.py` with PDF text extraction using pdfplumber
- LLM-based CV info extraction via Groq API
- Extracts name, email, skills, experience, keywords

### v0.2 — Job Scraper
- Added `src/scraper.py` with Adzuna and RemoteOK integration
- Keyword-based job fetching with relevance filtering
- Supports India-based and remote job listings