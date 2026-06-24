import requests
import os

def fetch_adzuna_jobs(keywords: list, location: str = "India", max_results: int = 10) -> list:
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    
    query = " ".join(keywords[:5])
    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1"
    
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": max_results,
        "what": query,
        "where": location,
        "content-type": "application/json"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    jobs = []
    for job in data.get("results", []):
        jobs.append({
            "title": job.get("title", ""),
            "company": job.get("company", {}).get("display_name", ""),
            "location": job.get("location", {}).get("display_name", ""),
            "description": job.get("description", ""),
            "url": job.get("redirect_url", ""),
            "salary_min": job.get("salary_min", 0),
            "salary_max": job.get("salary_max", 0),
            "source": "adzuna"
        })
    
    return jobs

def fetch_remoteok_jobs(keywords: list, max_results: int = 10) -> list:
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "cv-autopilot/1.0"}
    
    response = requests.get(url, headers=headers)
    data = response.json()[1:]
    
    keyword_set = set(k.lower() for k in keywords)
    jobs = []
    
    for job in data:
        tags = [t.lower() for t in job.get("tags", [])]
        title = job.get("position", "").lower()
        description = job.get("description", "").lower()
        
        match_count = sum(1 for k in keyword_set if k in tags or k in title or k in description)
        
        if match_count >= 2:
            jobs.append({
                "title": job.get("position", ""),
                "company": job.get("company", ""),
                "location": "Remote",
                "description": job.get("description", ""),
                "url": job.get("url", ""),
                "salary_min": 0,
                "salary_max": 0,
                "source": "remoteok"
            })
        
        if len(jobs) >= max_results:
            break
    
    return jobs

def fetch_all_jobs(keywords: list) -> list:
    jobs = []
    
    try:
        remote_jobs = fetch_remoteok_jobs(keywords)
        jobs += remote_jobs
        print(f"RemoteOK: {len(remote_jobs)} jobs found")
    except Exception as e:
        print(f"RemoteOK failed: {e}")
    
    try:
        adzuna_jobs = fetch_adzuna_jobs(keywords)
        jobs += adzuna_jobs
        print(f"Adzuna: {len(adzuna_jobs)} jobs found")
    except Exception as e:
        print(f"Adzuna failed: {e}")
    
    return jobs