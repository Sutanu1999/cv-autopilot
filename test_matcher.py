import os
from dotenv import load_dotenv
from groq import Groq
from src.parser import extract_text_from_pdf, extract_cv_info
from src.scraper import fetch_all_jobs
from src.matcher import rank_jobs

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

text = extract_text_from_pdf("data/cv.pdf")
info = extract_cv_info(text, client)

fetch_keywords = ["Data Engineer", "Python", "ETL", "PySpark"]
jobs = fetch_all_jobs(fetch_keywords)
ranked = rank_jobs(text, info["keywords"], jobs)

print(f"\nTop matched jobs for {info['name']}:\n")
for i, job in enumerate(ranked[:5], 1):
    print(f"--- Rank {i} ---")
    print(f"Title: {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Similarity: {job['similarity_score']}%")
    print(f"ATS Score: {job['ats_score']}%")
    print(f"Matched Keywords: {job['matched_keywords']}")
    print(f"Missing Keywords: {job['missing_keywords']}")
    print()