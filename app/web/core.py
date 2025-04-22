"""Core web module for primary web routes.

This module implements core web interface routes for the application,
handling primary pages like the landing page, about page, and other
central web content.
"""

from pathlib import Path

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.web.base_router import WebRouter

# Setup templates
templates_path = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))

core_web_router = WebRouter()


@core_web_router.get(
    "/",
    summary="Homepage",
    response_description="Welcome to MyResumo",
    response_class=HTMLResponse,
)
async def home(
    request: Request,
):
    """Render the homepage.

    This endpoint renders the main landing page with information about the
    application and a call-to-action to create a resume.

    Args:
        request: The incoming HTTP request

    Returns:
    -------
        HTMLResponse: The rendered home page
    """
    return templates.TemplateResponse("index.html", {"request": request})


@core_web_router.get(
    "/about",
    summary="About Us",
    response_description="Learn more about MyResumo",
    response_class=HTMLResponse,
)
async def about(
    request: Request,
):
    """Render the about page.

    This endpoint renders information about MyResumo, its features,
    and the team behind it.

    Args:
        request: The incoming HTTP request

    Returns:
    -------
        HTMLResponse: The rendered about page
    """
    return templates.TemplateResponse("about.html", {"request": request})


@core_web_router.get(
    "/contribution",
    summary="Contribution",
    response_description="Get involved with MyResumo development",
    response_class=HTMLResponse,
)
async def contribution(
    request: Request,
):
    """Render the contribution page.

    Args:
        request: The FastAPI request object

    Returns:
    -------
        HTMLResponse: Rendered HTML template for contribution page
    """
    return templates.TemplateResponse("contribution.html", {"request": request})
