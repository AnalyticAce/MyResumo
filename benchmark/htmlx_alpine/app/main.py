from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import time
from pathlib import Path
import json

app = FastAPI(title="MyResumo")

# Mount static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/optimize-resume", response_class=HTMLResponse)
async def optimize_resume(request: Request):
    # Simulate processing time
    time.sleep(1)
    # Mock optimized resume HTML
    optimized_html = """
    <p><strong>John Doe</strong><br>Software Engineer<br>john.doe@email.com</p>
    <p><strong>Experience</strong><br>Senior Developer, ABC Tech (2020-Present)<br>
    - <span class="text-green-600">Developed scalable web applications using React and Node.js</span><br>
    - <span class="text-green-600">Implemented CI/CD pipelines for automated testing and deployment</span><br>
    - <span class="text-green-600">Collaborated with cross-functional teams on AWS-based solutions</span></p>
    <p><strong>Skills</strong><br>
    JavaScript, React, Node.js, Git, Agile, <span class="text-green-600">Python, AWS, Docker</span></p>
    <p><strong>Education</strong><br>BS Computer Science, University of Technology (2016-2020)</p>
    """
    return optimized_html

@app.post("/api/download-resume")
async def download_resume(request: Request):
    # In a real implementation, this would generate and return the file
    # For demo purposes, we'll just return a JSON response
    return {"status": "success", "message": "Download initiated"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)