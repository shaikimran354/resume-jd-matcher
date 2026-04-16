from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from parser import extract_text
from matcher import match_resume_jd

app = FastAPI(title="Resume-JD Matcher API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Resume-JD Matcher API is running"}

@app.post("/match")
async def match(
    resume: UploadFile = File(...),
    jd_text: str = Form(...)
):
    resume_bytes = await resume.read()
    resume_text = extract_text(resume_bytes, resume.filename)

    if not resume_text:
        return {"error": "Could not extract text from resume. Please upload a valid PDF or DOCX."}

    result = match_resume_jd(resume_text, jd_text)
    return result