from fastapi import APIRouter, Depends, HTTPException
from app.db.resume_repo import ResumeRepository
from app.routers.models import User, UserInDB, Resume
from app.utils.auth_utils import get_current_active_user

resume_router = APIRouter(
    prefix="/api/v1/resume",
    tags=["Resume Management"],
    responses={
        404: {"description": "Endpoint not found"},
        403: {"description": "Forbidden access"},
        200: {"description": "Success response"},
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized access"},
        409: {"description": "username already exists"},
    }
)

resume_repo = ResumeRepository("myresumo")

@resume_router.post("/create", response_model=User)
async def create_resume(
        data: Resume,
        current_user: UserInDB = Depends(get_current_active_user)
    ):
    try:
        created_resume = await resume_repo.insert_one(data.model_dump())
        if created_resume is None:
            raise HTTPException(status_code=500, detail="Failed to create resume")
        return created_resume
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

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