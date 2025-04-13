from fastapi import APIRouter, HTTPException, Request, status
from app.web.base_router import WebRouter
from fastapi.templating import Jinja2Templates

web_router = WebRouter()
templates = Jinja2Templates(directory="templates")

@web_router.get(
    "/dashboard",
    summary="Dashboard",
    response_description="Welcome to MyResumo",
)
async def dashboard(
    request: Request,
):
    pass

@web_router.get(
    "/settings",
    summary="Settings",
    response_description="Manage your settings",
)
async def settings(
    request: Request,
):
    pass
