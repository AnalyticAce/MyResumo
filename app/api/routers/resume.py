from typing import List, Dict, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Request, status, UploadFile, File, Form, Body
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.database.models.resume import Resume, ResumeData
from app.database.repositories.resume_repository import ResumeRepository
from app.services.ai.model_ai import AtsResumeOptimizer
from app.services.resume.latex_generator import LaTeXGenerator
from app.utils.file_handling import extract_text_from_pdf, save_pdf_file, create_temporary_pdf
import os
import tempfile
from pathlib import Path
import secrets
from datetime import datetime
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Request and response models
class CreateResumeRequest(BaseModel):
    user_id: str
    title: str
    original_content: str
    job_description: str


class OptimizeResumeRequest(BaseModel):
    job_description: str


class ResumeSummary(BaseModel):
    id: str
    title: str
    ats_score: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class OptimizationResponse(BaseModel):
    resume_id: str
    ats_score: int
    optimized_data: Dict[str, Any]


# Initialize the API router
resume_router = APIRouter(
    prefix="/api/resume",
    tags=["Resume"]
)


# Helper function to get repository instance
async def get_resume_repository(request: Request) -> ResumeRepository:
    return ResumeRepository()


@resume_router.post(
    "/",
    response_model=Dict[str, str],
    summary="Create a resume",
    response_description="Resume created successfully",
)
async def create_resume(
    request: Request,
    file: UploadFile = File(...),
    title: str = Form(...),
    job_description: str = Form(...),
    user_id: str = Form(...),
    repo: ResumeRepository = Depends(get_resume_repository),
):
    try:
        pdf_content = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(pdf_content)
            temp_file_path = temp_file.name
        try:
            resume_text = extract_text_from_pdf(temp_file_path)
        finally:
            os.unlink(temp_file_path)
        new_resume = Resume(
            user_id=user_id,
            title=title,
            original_content=resume_text,
            job_description=job_description,
        )
        resume_id = await repo.create_resume(new_resume)
        if not resume_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create resume"
            )
        return {"id": resume_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating resume: {str(e)}"
        )


@resume_router.get(
    "/{resume_id}",
    response_model=Dict[str, Any],
    summary="Get a resume",
    response_description="Resume retrieved successfully",
)
async def get_resume(
    resume_id: str,
    request: Request,
    repo: ResumeRepository = Depends(get_resume_repository),
):
    resume_data = await repo.get_resume_by_id(resume_id)
    if not resume_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found"
        )
    resume_data["id"] = str(resume_data.pop("_id"))
    return resume_data


@resume_router.get(
    "/user/{user_id}",
    response_model=List[ResumeSummary],
    summary="Get all resumes for a user",
    response_description="Resumes retrieved successfully",
)
async def get_user_resumes(
    user_id: str,
    request: Request,
    repo: ResumeRepository = Depends(get_resume_repository),
):
    resumes = await repo.get_resumes_by_user_id(user_id)
    formatted_resumes = []
    for resume in resumes:
        formatted_resumes.append({
            "id": str(resume.get("_id")),
            "title": resume.get("title"),
            "ats_score": resume.get("ats_score"),
            "created_at": resume.get("created_at"),
            "updated_at": resume.get("updated_at"),
        })
    return formatted_resumes


@resume_router.put(
    "/{resume_id}",
    response_model=Dict[str, bool],
    summary="Update a resume",
    response_description="Resume updated successfully",
)
async def update_resume(
    resume_id: str,
    update_data: Dict[str, Any] = Body(...),
    request: Request = None,
    repo: ResumeRepository = Depends(get_resume_repository),
):
    resume = await repo.get_resume_by_id(resume_id)
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found"
        )
    success = await repo.update_resume(resume_id, update_data)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update resume"
        )
    return {"success": True}


@resume_router.delete(
    "/{resume_id}",
    response_model=Dict[str, bool],
    summary="Delete a resume",
    response_description="Resume deleted successfully",
)
async def delete_resume(
    resume_id: str,
    request: Request = None,
    repo: ResumeRepository = Depends(get_resume_repository),
):
    resume = await repo.get_resume_by_id(resume_id)
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found"
        )
    success = await repo.delete_resume(resume_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete resume"
        )
    return {"success": True}


@resume_router.post(
    "/{resume_id}/optimize",
    response_model=OptimizationResponse,
    summary="Optimize a resume with AI",
    response_description="Resume optimized successfully",
)
async def optimize_resume(
    resume_id: str,
    optimization_request: OptimizeResumeRequest,
    request: Request,
    repo: ResumeRepository = Depends(get_resume_repository),
):
    logger.info(f"Starting resume optimization for resume_id: {resume_id}")
    
    # 1. Retrieve resume
    logger.info(f"Retrieving resume with ID: {resume_id}")
    resume = await repo.get_resume_by_id(resume_id)
    if not resume:
        logger.warning(f"Resume not found with ID: {resume_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found"
        )
    logger.info(f"Successfully retrieved resume: {resume.get('title', 'Untitled')}")
    
    # 2. Get API configuration
    logger.info("Retrieving API configuration")
    api_key = os.getenv("OPENAI_API_KEY")
    api_base_url = os.getenv("OPENAI_API_BASE_URL")
    model_name = os.getenv("OPENAI_MODEL_NAME")
    
    # Log API configuration (safely)
    logger.info(f"API configuration - model_name: {model_name or 'Not set'}")
    logger.info(f"API configuration - api_base_url: {api_base_url or 'Not set'}")
    logger.info(f"API Key present: {bool(api_key)}")
    
    if not api_key:
        logger.warning("API key not found in environment variables, attempting to get from app state")
        try:
            api_key = request.app.state.config.AI_API_KEY
            logger.info("Successfully retrieved API key from app state")
        except Exception as config_error:
            logger.error(f"Failed to retrieve API key from app state: {str(config_error)}")
            logger.error(f"Config error details: {traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI API key not configured"
            )
    
    # 3. Initialize optimizer
    logger.info("Initializing AtsResumeOptimizer")
    optimizer = AtsResumeOptimizer(
        model_name=model_name,
        resume=resume["original_content"],
        api_key=api_key,
        api_base=api_base_url,
    )
    
    # 4. Get job description
    job_description = optimization_request.job_description or resume.get("job_description", "")
    logger.info(f"Job description length: {len(job_description)} characters")
    
    if not job_description:
        logger.warning("Job description is empty")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description is required for optimization"
        )
    
    try:
        # 5. Generate optimized resume
        logger.info("Calling AI service to generate optimized resume")
        result = optimizer.generate_ats_optimized_resume_json(job_description)
        
        # 6. Check for errors in result
        if "error" in result:
            logger.error(f"AI service returned an error: {result.get('error')}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI optimization error: {result['error']}"
            )
        
        # 7. Log the structure of the result (without exposing sensitive data)
        logger.info("AI service returned result successfully")
        logger.info(f"Result keys: {list(result.keys() if isinstance(result, dict) else [])}")
        
        # 8. Calculate score
        logger.info("Calculating ATS score from result")
        score_bases = {
            "skills_match": len(result.get("user_information", {}).get("skills", {}).get("hard_skills", [])),
            "experiences": len(result.get("user_information", {}).get("experiences", [])),
            "education": len(result.get("user_information", {}).get("education", [])),
            "projects": len(result.get("projects", [])),
        }
        logger.info(f"Score bases: {score_bases}")
        
        base_score = 50
        max_additional = 45
        completeness_score = sum(min(value, 5) for value in score_bases.values()) / (5 * len(score_bases))
        ats_score = int(base_score + (completeness_score * max_additional))
        logger.info(f"Calculated ATS score: {ats_score}")
        
        # 9. Parse and validate result
        logger.info("Parsing result into ResumeData model")
        try:
            optimized_data = ResumeData.parse_obj(result)
            logger.info("Successfully validated result through Pydantic model")
        except Exception as validation_error:
            logger.error(f"Failed to parse result into ResumeData model: {str(validation_error)}")
            logger.error(f"Validation error details: {traceback.format_exc()}")
            logger.debug(f"Problematic data: {result}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error parsing AI response: {str(validation_error)}"
            )
        
        # 10. Update database
        logger.info(f"Updating resume {resume_id} with optimized data")
        try:
            await repo.update_optimized_data(resume_id, optimized_data, ats_score)
            logger.info("Successfully updated resume with optimized data")
        except Exception as db_error:
            logger.error(f"Database error during update: {str(db_error)}")
            logger.error(f"Database error details: {traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error during update: {str(db_error)}"
            )
        
        # 11. Return success response
        logger.info(f"Resume optimization completed successfully for resume_id: {resume_id}")
        return {
            "resume_id": resume_id,
            "ats_score": ats_score,
            "optimized_data": result
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as they're already properly formatted
        raise
    except Exception as e:
        # Log the full stack trace for any other exception
        logger.error(f"Unexpected error during resume optimization: {str(e)}")
        logger.error(f"Error details: {traceback.format_exc()}")
        
        # Check for specific error types to provide better error messages
        if "API key" in str(e).lower() or "authentication" in str(e).lower():
            logger.error("AI service authentication error")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error authenticating with AI service. Please check API configuration."
            )
        elif "timeout" in str(e).lower() or "time" in str(e).lower():
            logger.error("AI service timeout error")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI service request timed out. Please try again later."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error during resume optimization: {str(e)}"
            )


@resume_router.get(
    "/{resume_id}/download",
    summary="Download a resume as PDF",
    response_description="Resume downloaded successfully",
)
async def download_resume(
    resume_id: str,
    use_optimized: bool = True,
    template: str = "resume_template.tex",
    request: Request = None,
    repo: ResumeRepository = Depends(get_resume_repository),
):
    resume = await repo.get_resume_by_id(resume_id)
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found"
        )
    if use_optimized and not resume.get("optimized_data"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Optimized resume data not available. Please optimize the resume first."
        )
    try:
        latex_dir = Path("data/sample_latex_templates")
        if not latex_dir.exists():
            latex_dir = Path("app/services/resume/latex_templates")
            if not latex_dir.exists():
                latex_dir.mkdir(parents=True, exist_ok=True)
        generator = LaTeXGenerator(str(latex_dir))
        if use_optimized:
            json_data = resume["optimized_data"]
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Downloading original resume as PDF is not supported. Please optimize first."
            )
        if isinstance(json_data, str):
            generator.parse_json_from_string(json_data)
        else:
            generator.json_data = json_data
        latex_content = generator.generate_from_template(template)
        if not latex_content:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate LaTeX content"
            )
        pdf_path = create_temporary_pdf(latex_content)
        if not pdf_path:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create PDF"
            )
        filename = f"{resume.get('title', 'resume')}_{secrets.token_hex(4)}.pdf"
        return FileResponse(
            path=pdf_path, 
            filename=filename,
            media_type="application/pdf",
            background=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating PDF: {str(e)}"
        )


@resume_router.get(
    "/{resume_id}/preview",
    summary="Preview a resume",
    response_description="Resume previewed successfully",
)
async def preview_resume(
    resume_id: str,
    request: Request,
    repo: ResumeRepository = Depends(get_resume_repository),
):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Resume preview not implemented. Use the download endpoint to generate a PDF."
    )