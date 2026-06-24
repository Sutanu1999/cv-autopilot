import os
from dotenv import load_dotenv
from groq import Groq
from src.parser import extract_text_from_pdf, extract_cv_info

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

pdf_path = "data/cv.pdf"  # rename your CV file to cv.pdf

text = extract_text_from_pdf(pdf_path)
print("=== Extracted Text (first 500 chars) ===")
print(text[:500])

print("\n=== Parsed CV Info ===")
info = extract_cv_info(text, client)
for key, value in info.items():
    print(f"{key}: {value}")