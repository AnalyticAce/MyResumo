from fastapi import APIRouter, HTTPException, Request, status
from app.web.base_router import WebRouter
from fastapi.templating import Jinja2Templates

core_web_router = WebRouter()
templates = Jinja2Templates(directory="templates")

@core_web_router.get(
    "/",
    summary="Homepage",
    response_description="Welcome to MyResumo",
)
async def home(
    request: Request,
):
    pass

@core_web_router.get(
    "/about",
    summary="About Us",
    response_description="Learn more about MyResumo",
)
async def about(
    request: Request,
):
    pass

@core_web_router.get(
    "/contact",
    summary="Contact Us",
    response_description="Get in touch with MyResumo Maintainer and Contributors",
)
async def contact(
    request: Request,
):
    pass
