import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from parser import extract_text_from_pdf, extract_cv_info
from scraper import fetch_all_jobs
from matcher import rank_jobs
from rewriter import rewrite_cv, generate_cover_letter, save_outputs

load_dotenv()

st.set_page_config(page_title="CV Autopilot", page_icon="🚀", layout="wide")
st.title("🚀 CV Autopilot")
st.caption("Upload your CV, find matching jobs, and get a tailored CV + cover letter instantly.")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

with st.sidebar:
    st.header("⚙️ Settings")
    location = st.text_input("Job Location", value="India")
    max_jobs = st.slider("Max jobs to fetch", 5, 20, 10)
    fetch_keywords = st.text_input("Search Keywords", value="Data Engineer, Python, ETL")

uploaded_file = st.file_uploader("Upload your CV (PDF)", type=["pdf"])

if uploaded_file:
    os.makedirs("../data", exist_ok=True)
    with open("../data/temp_cv.pdf", "wb") as f:
        f.write(uploaded_file.read())
    
    with st.spinner("Parsing your CV..."):
        cv_text = extract_text_from_pdf("../data/temp_cv.pdf")
        cv_info = extract_cv_info(cv_text, client)
    
    st.success(f"CV parsed for **{cv_info['name']}** — {cv_info['experience_years']} years experience")
    
    with st.expander("View extracted CV info"):
        st.json(cv_info)
    
    if st.button("🔍 Find Matching Jobs", type="primary"):
        keywords = [k.strip() for k in fetch_keywords.split(",")]
        
        with st.spinner("Fetching jobs..."):
            jobs = fetch_all_jobs(keywords)
        
        with st.spinner("Ranking jobs by relevance..."):
            ranked = rank_jobs(cv_text, cv_info["keywords"], jobs)
        
        st.session_state["ranked"] = ranked
        st.session_state["cv_text"] = cv_text
        st.session_state["cv_info"] = cv_info

if "ranked" in st.session_state:
    ranked = st.session_state["ranked"]
    cv_text = st.session_state["cv_text"]
    
    st.subheader(f"Found {len(ranked)} matching jobs")
    
    for i, job in enumerate(ranked):
        with st.expander(f"**{job['title']}** at {job['company']} — Similarity: {job['similarity_score']}% | ATS: {job['ats_score']}%"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Location:** {job['location']}")
                st.markdown(f"**Source:** {job['source']}")
                st.markdown(f"**Apply:** [Link]({job['url']})")
            with col2:
                st.markdown(f"**Matched Keywords:** {', '.join(job['matched_keywords'])}")
                st.markdown(f"**Missing Keywords:** {', '.join(job['missing_keywords'])}")
            
            if st.button(f"✍️ Rewrite CV for this job", key=f"rewrite_{i}"):
                with st.spinner("Rewriting CV and generating cover letter..."):
                    rewritten = rewrite_cv(cv_text, job["description"], job["missing_keywords"], client)
                    cover_letter = generate_cover_letter(cv_text, job, client)
                    paths = save_outputs(rewritten, cover_letter, job)
                
                st.session_state[f"paths_{i}"] = paths
            
            if f"paths_{i}" in st.session_state:
                paths = st.session_state[f"paths_{i}"]
                st.success("Done! Files saved.")
                
                col1, col2 = st.columns(2)
                with col1:
                    with open(paths["cv_path"], "rb") as f:
                        st.download_button("📄 Download Rewritten CV", f, file_name=os.path.basename(paths["cv_path"]), key=f"dl_cv_{i}")
                with col2:
                    with open(paths["cover_letter_path"], "rb") as f:
                        st.download_button("📝 Download Cover Letter", f, file_name=os.path.basename(paths["cover_letter_path"]), key=f"dl_cl_{i}")