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

### v0.3 — Job Matcher
- Added `src/matcher.py` with sentence-transformers similarity scoring
- ATS keyword matching with matched/missing keyword breakdown
- Jobs ranked by similarity score
- Fixed keyword extraction to use short technical terms

### v0.4 — CV Rewriter & Cover Letter
- Added `src/rewriter.py` with LLM-based CV rewriting
- Incorporates missing ATS keywords naturally into existing experience
- Auto-generates a tailored cover letter for each job

### v0.5 — Proper File Output
- CV saved as `.pdf` using reportlab
- Cover letter saved as `.pdf` using reportlab
- Files named after job title and company for easy tracking

### v0.6 — Streamlit UI
- Added `src/main.py` with full Streamlit interface
- Upload CV, fetch jobs, view ranked results with ATS and similarity scores
- Rewrite CV and generate cover letter for any job with one click
- Download rewritten CV and cover letter as PDF directly from UI
- Fixed download button state persistence using session state