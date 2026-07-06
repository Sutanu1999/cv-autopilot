from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm
import os

def rewrite_cv(cv_text: str, job_description: str, missing_keywords: list, client) -> str:
    prompt = f"""
You are an expert CV writer. Your task is to rewrite the CV below to better match the job description.

Rules:
- Only add or rephrase existing experience, do NOT fabricate anything
- Naturally incorporate the missing keywords where relevant
- Keep the same structure and sections
- Do not change name, contact info, or education
- Return the full rewritten CV text only, no explanation

Missing Keywords to incorporate: {", ".join(missing_keywords)}

Job Description:
{job_description}

Original CV:
{cv_text}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    return response.choices[0].message.content

def generate_cover_letter(cv_text: str, job: dict, client) -> str:
    prompt = f"""
Write a short, professional cover letter for the following job based on the CV provided.

Rules:
- Maximum 3 paragraphs
- First paragraph: why you're interested in this role
- Second paragraph: 2-3 most relevant skills/experiences from the CV
- Third paragraph: closing statement
- Do not use generic filler phrases
- Return the cover letter text only

Job Title: {job['title']}
Company: {job['company']}
Job Description: {job['description']}

CV:
{cv_text}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    
    return response.choices[0].message.content

def save_cv_as_pdf(rewritten_cv: str, path: str):
    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    styles = getSampleStyleSheet()
    
    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Normal"],
        fontSize=13,
        leading=18,
        spaceBefore=12,
        spaceAfter=4,
        fontName="Helvetica-Bold"
    )
    
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        spaceAfter=6
    )
    
    story = []
    for line in rewritten_cv.split("\n"):
        line = line.strip()
        if not line:
            story.append(Spacer(1, 0.2*cm))
            continue
        
        if line.isupper() or (len(line) < 40 and line.endswith(":")):
            story.append(Paragraph(line, heading_style))
        else:
            story.append(Paragraph(line, body_style))
    
    doc.build(story)

def save_cover_letter_as_pdf(cover_letter: str, path: str):
    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=11,
        leading=16,
        spaceAfter=12
    )
    
    story = []
    for para in cover_letter.split("\n\n"):
        para = para.strip()
        if para:
            story.append(Paragraph(para.replace("\n", " "), body_style))
            story.append(Spacer(1, 0.3*cm))
    
    doc.build(story)

def save_outputs(rewritten_cv: str, cover_letter: str, job: dict) -> dict:
    os.makedirs("logs", exist_ok=True)
    
    company = job['company'].replace(" ", "_").replace("/", "_")
    title = job['title'].replace(" ", "_").replace("/", "_")
    base = f"logs/{title}_{company}"
    
    cv_path = f"{base}_cv.pdf"
    cl_path = f"{base}_cover_letter.pdf"
    
    save_cv_as_pdf(rewritten_cv, cv_path)
    save_cover_letter_as_pdf(cover_letter, cl_path)
    
    return {"cv_path": cv_path, "cover_letter_path": cl_path}