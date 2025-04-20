from fastapi import APIRouter, HTTPException, Request, status
from app.web.base_router import WebRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

core_web_router = WebRouter()
templates = Jinja2Templates(directory="app/templates")

@core_web_router.get(
    "/",
    summary="Homepage",
    response_description="Welcome to MyResumo",
    response_class=HTMLResponse,
)
async def home(
    request: Request,
):
    """
    Render the homepage.
    
    This endpoint renders the main landing page with information about the 
    application and a call-to-action to create a resume.
    
    Args:
        request: The incoming HTTP request
        
    Returns:
        HTMLResponse: The rendered home page
    """
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@core_web_router.get(
    "/about",
    summary="About Us",
    response_description="Learn more about MyResumo",
    response_class=HTMLResponse,
)
async def about(
    request: Request,
):
    """
    Render the about page.
    
    This endpoint renders information about MyResumo, its features,
    and the team behind it.
    
    Args:
        request: The incoming HTTP request
        
    Returns:
        HTMLResponse: The rendered about page
    """
    return templates.TemplateResponse(
        "about.html",
        {"request": request}
    )

@core_web_router.get(
    "/contact",
    summary="Contact Us",
    response_description="Get in touch with MyResumo Maintainer and Contributors",
    response_class=HTMLResponse,
)
async def contact(
    request: Request,
):
    """
    Render the contact page.
    
    This endpoint renders a form and information for contacting the 
    MyResumo team.
    
    Args:
        request: The incoming HTTP request
        
    Returns:
        HTMLResponse: The rendered contact page
    """
    return templates.TemplateResponse(
        "contact.html",
        {"request": request}
    )
