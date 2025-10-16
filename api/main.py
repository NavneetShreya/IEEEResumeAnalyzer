# api/main.py

from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import JSONResponse
import shutil
import os
from pathlib import Path
from resume_analyzer import extract_text_from_pdf, extract_skills
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ Initialize FastAPI App
app = FastAPI(
    title="IEEE Resume Analyzer API",
    description="API that compares resume skills with job description and returns a similarity score.",
    version="1.0.0"
)

# ✅ Upload Directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# ✅ Root Endpoint
@app.get("/")
def root():
    return {"message": "Resume Analyzer API is running successfully 🚀"}


# ✅ Main Analysis Endpoint
@app.post("/analyze_resume")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Endpoint to analyze resume against a job description.
    Accepts:
    - resume (PDF file)
    - job_description (string)
    """

    try:
        # --- Step 1: Save uploaded resume temporarily ---
        resume_path = UPLOAD_DIR / resume.filename
        with open(resume_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)

        # --- Step 2: Extract resume text and skills ---
        resume_text = extract_text_from_pdf(resume_path)
        resume_skills = extract_skills(resume_text)

        # --- Step 3: Extract JD skills ---
        jd_skills = extract_skills(job_description)

        # --- Step 4: Compute Similarity ---
        if not resume_skills or not jd_skills:
            return JSONResponse(
                status_code=400,
                content={"error": "Could not extract skills from resume or JD."}
            )

        # Convert skills into text format for cosine similarity
        vectorizer = CountVectorizer().fit_transform([
            " ".join(resume_skills),
            " ".join(jd_skills)
        ])
        similarity = cosine_similarity(vectorizer)[0][1] * 100

        # --- Step 5: Find matching skills ---
        matching_skills = list(set(skill.lower() for skill in resume_skills) &
                               set(skill.lower() for skill in jd_skills))

        # --- Step 6: Prepare and return response ---
        response = {
            "resume_skills": resume_skills,
            "jd_skills": jd_skills,
            "matching_skills": matching_skills,
            "similarity_score": round(similarity, 2)
        }

        # Clean up uploaded file
        os.remove(resume_path)

        return JSONResponse(content=response)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
