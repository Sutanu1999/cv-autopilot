import os
from dotenv import load_dotenv
from groq import Groq
from src.parser import extract_text_from_pdf, extract_cv_info
from src.scraper import fetch_all_jobs
from src.matcher import rank_jobs
from src.rewriter import rewrite_cv, generate_cover_letter, save_outputs

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

text = extract_text_from_pdf("data/cv.pdf")
info = extract_cv_info(text, client)

fetch_keywords = ["Data Engineer", "Python", "ETL", "PySpark"]
jobs = fetch_all_jobs(fetch_keywords)
ranked = rank_jobs(text, info["keywords"], jobs)

top_job = ranked[0]
print(f"Rewriting CV for: {top_job['title']} at {top_job['company']}")
print(f"Missing Keywords: {top_job['missing_keywords']}\n")

rewritten = rewrite_cv(text, top_job["description"], top_job["missing_keywords"], client)
print("=== Rewritten CV (first 500 chars) ===")
print(rewritten[:500])

print("\n=== Cover Letter ===")
cover_letter = generate_cover_letter(text, top_job, client)
print(cover_letter)

paths = save_outputs(rewritten, cover_letter, top_job)
print(f"\nSaved to:")
print(f"CV: {paths['cv_path']}")
print(f"Cover Letter: {paths['cover_letter_path']}")