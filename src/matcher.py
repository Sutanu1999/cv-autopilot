from sentence_transformers import SentenceTransformer, util
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_similarity(cv_text: str, job_description: str) -> float:
    cv_embedding = model.encode(cv_text, convert_to_tensor=True)
    jd_embedding = model.encode(job_description, convert_to_tensor=True)
    score = util.cos_sim(cv_embedding, jd_embedding)
    return round(float(score[0][0]) * 100, 2)

def compute_ats_score(cv_keywords: list, job_description: str) -> dict:
    jd_lower = job_description.lower()
    matched = [k for k in cv_keywords if k.lower() in jd_lower]
    missing = [k for k in cv_keywords if k.lower() not in jd_lower]
    score = round(len(matched) / len(cv_keywords) * 100, 2) if cv_keywords else 0
    
    return {
        "score": score,
        "matched_keywords": matched,
        "missing_keywords": missing
    }

def rank_jobs(cv_text: str, cv_keywords: list, jobs: list) -> list:
    ranked = []
    
    for job in jobs:
        jd = job.get("description", "")
        if not jd:
            continue
        
        similarity = compute_similarity(cv_text, jd)
        ats = compute_ats_score(cv_keywords, jd)
        
        ranked.append({
            **job,
            "similarity_score": similarity,
            "ats_score": ats["score"],
            "matched_keywords": ats["matched_keywords"],
            "missing_keywords": ats["missing_keywords"]
        })
    
    ranked.sort(key=lambda x: x["similarity_score"], reverse=True)
    return ranked