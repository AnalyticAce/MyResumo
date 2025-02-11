from fastapi import APIRouter, Depends, HTTPException
from app.db.resume_repo import ResumeRepository
from app.routers.models import User, UserInDB, Resume
from app.utils.auth_utils import get_current_active_user

resume_router = APIRouter(
    prefix="/api/v1/resume",
    tags=["Resume Management"]
)

resume_repo = ResumeRepository("myresumo")

@resume_router.get("/create", response_model=User)
async def create_resume(
        resume: Resume,
        current_user: UserInDB = Depends(get_current_active_user)
    ):
    resume = await resume_repo.insert_one(resume.model_dump())
    
    if resume is None:
        raise HTTPException(status_code=500, detail="Failed to create resume")

@resume_router.get("/list", response_model=User)
async def list_resumes(current_user: UserInDB = Depends(get_current_active_user)):
    pass

@resume_router.put("/update", response_model=User)
async def update_resume(current_user: UserInDB = Depends(get_current_active_user)):
    pass

@resume_router.delete("/delete", response_model=User)
async def delete_resume(current_user: UserInDB = Depends(get_current_active_user)):
    pass

@resume_router.get("/get/{_id}", response_model=User)
async def get_resume(
        _id: str,
        current_user: UserInDB = Depends(get_current_active_user)
    ):
    pass