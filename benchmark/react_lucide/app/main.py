# app/main.py

from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List
import json
import time
from pathlib import Path
import uuid

app = FastAPI(title="MyResumo API")

# Add CORS middleware to allow your React frontend to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResumeAnalysisRequest(BaseModel):
    resume_text: Optional[str] = None
    job_description: Optional[str] = None

class OptimizeResumeRequest(BaseModel):
    resume_text: str
    job_description: str

class DownloadResumeRequest(BaseModel):
    resume_text: str
    format: str

@app.post("/api/analyze-resume")
async def analyze_resume(request: ResumeAnalysisRequest):
    """
    Analyze resume against job description and return match score and suggestions
    """
    # Simulate processing time
    time.sleep(2)
    
    # Mock response data
    return {
        "match_score": 65,
        "matched_skills": ["JavaScript", "React", "Node.js"],
        "missing_skills": ["Python", "AWS", "Docker", "TypeScript", "GraphQL"],
        "suggestions": [
            {
                "id": 1,
                "title": "Add Python experience",
                "description": "The job requires Python but it's not mentioned in your resume. If you have experience with Python, add it to your skills section."
            },
            {
                "id": 2,
                "title": "Highlight AWS experience",
                "description": "AWS knowledge is required. Include any AWS experience you have or mention relevant cloud experience."
            },
            {
                "id": 3,
                "title": "Add Docker to your skills",
                "description": "Docker experience is required. If you have containerization experience, add it to your skills section."
            }
        ]
    }

@app.post("/api/optimize-resume")
async def optimize_resume(request: OptimizeResumeRequest):
    """
    Generate an optimized version of the resume
    """
    # Simulate processing time
    time.sleep(1)
    
    # Mock optimized resume HTML
    optimized_html = """
    <p><strong>John Doe</strong><br>Software Engineer<br>john.doe@email.com</p>
    <p><strong>Experience</strong><br>Senior Developer, ABC Tech (2020-Present)<br>
    - Developed scalable web applications using React and Node.js<br>
    - Implemented CI/CD pipelines for automated testing and deployment<br>
    - Collaborated with cross-functional teams on AWS-based solutions</p>
    <p><strong>Skills</strong><br>
    JavaScript, React, Node.js, Git, Agile, Python, AWS, Docker</p>
    <p><strong>Education</strong><br>BS Computer Science, University of Technology (2016-2020)</p>
    """
    
    return {"optimized_content": optimized_html}

@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Handle resume file upload
    """
    # Create a temporary file to store the uploaded content
    file_location = f"tmp/{file.filename}"
    file_path = Path(file_location)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # In a real implementation, you would parse the file here
    # For demo purposes, return mock content
    mock_resume_content = "<p><strong>John Doe</strong><br>Software Engineer<br>john.doe@email.com</p><p><strong>Experience</strong><br>Senior Developer, ABC Tech (2020-Present)<br>- Developed web applications using React and Node.js<br>- Implemented CI/CD pipelines</p><p><strong>Skills</strong><br>JavaScript, React, Node.js, Git, Agile</p><p><strong>Education</strong><br>BS Computer Science, University of Technology (2016-2020)</p>"
    
    return {"filename": file.filename, "resume_content": mock_resume_content}

@app.post("/api/upload-job-description")
async def upload_job_description(file: UploadFile = File(...)):
    """
    Handle job description file upload
    """
    # Create a temporary file to store the uploaded content
    file_location = f"tmp/{file.filename}"
    file_path = Path(file_location)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # In a real implementation, you would parse the file here
    # For demo purposes, return mock content
    mock_job_description = "We are looking for a skilled Software Engineer with experience in React, Node.js, and Python. The ideal candidate should have knowledge of AWS, CI/CD, and Docker. Experience with TypeScript and GraphQL is preferred."
    
    return {"filename": file.filename, "job_description": mock_job_description}

@app.post("/api/download-resume")
async def download_resume(request: DownloadResumeRequest):
    """
    Generate and download the resume in the requested format
    """
    # In a real implementation, you would generate the file in the requested format
    # For demo purposes, we'll just return a success message
    
    return {"status": "success", "message": f"Resume downloaded in {request.format} format"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)