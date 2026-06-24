from dotenv import load_dotenv
from src.scraper import fetch_all_jobs

load_dotenv()

keywords = ["Data Engineer", "Python", "ETL", "PySpark"]
jobs = fetch_all_jobs(keywords)

print(f"\nTotal jobs found: {len(jobs)}\n")
for i, job in enumerate(jobs[:5], 1):
    print(f"--- Job {i} ---")
    print(f"Title: {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Location: {job['location']}")
    print(f"URL: {job['url']}")
    print()