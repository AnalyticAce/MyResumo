from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse

resume_router = APIRouter(
    prefix="/api/resume",
    tags=["Resume"]
)

@resume_router.post(
    "/",
    summary="Create a resume",
    response_description="Resume created successfully",
)
async def create_resume(
    request: Request,
):
    pass

@resume_router.get(
    "/{resume_id}",
    summary="Get a resume",
    response_description="Resume retrieved successfully",
)
async def get_resume(
    resume_id: str,
    request: Request,
):
    pass

@resume_router.put(
    "/{resume_id}",
    summary="Update a resume",
    response_description="Resume updated successfully",
)
async def update_resume(
    resume_id: str,
    request: Request,
):
    pass

@resume_router.delete(
    "/{resume_id}",
    summary="Delete a resume",
    response_description="Resume deleted successfully",
)
async def delete_resume(
    resume_id: str,
    request: Request,
):
    pass

@resume_router.get(
    "/{resume_id}/download",
    summary="Download a resume",
    response_description="Resume downloaded successfully",
)
async def download_resume(
    resume_id: str,
    request: Request,
):
    pass

@resume_router.get(
    "/{resume_id}/preview",
    summary="Preview a resume",
    response_description="Resume previewed successfully",
)
async def preview_resume(
    resume_id: str,
    request: Request,
):
    pass