import pdfplumber
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    return text.strip()

def extract_cv_info(text: str, client) -> dict:
    prompt = f"""
You are a CV parser. Extract the following from the CV text below and return as JSON only, no explanation:
{{
  "name": "",
  "email": "",
  "phone": "",
  "skills": [],
  "experience_years": 0,
  "current_role": "",
  "education": "",
  "keywords": []
}}

CV Text:
{text}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    
    import json
    raw = response.choices[0].message.content
    start = raw.find("{")
    end = raw.rfind("}") + 1
    return json.loads(raw[start:end])