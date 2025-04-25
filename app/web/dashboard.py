"""Dashboard web module for user-specific interfaces.

This module implements the dashboard interface routes, handling user-specific
views such as resume management, profile settings, and personalized features
that require user context.
"""

from fastapi import Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.web.base_router import WebRouter

web_router = WebRouter()
templates = Jinja2Templates(directory="app/templates")


@web_router.get(
    "/dashboard",
    summary="Dashboard",
    response_description="User dashboard showing resumes and statistics",
    response_class=HTMLResponse,
)
async def dashboard(
    request: Request,
):
    """Render the user dashboard.

    This endpoint displays the user's resume collection, optimization statistics,
    and actions they can take to create or optimize resumes.

    Args:
        request: The incoming HTTP request

    Returns:
    -------
        HTMLResponse: The rendered dashboard page
    """
    return templates.TemplateResponse("dashboard.html", {"request": request})


@web_router.get(
    "/create",
    summary="Create Resume",
    response_description="Create a new resume",
    response_class=HTMLResponse,
)
async def create_resume(
    request: Request,
):
    """Render the resume creation page.

    This endpoint displays the form for creating a new resume, including
    file upload for the original resume and input for job descriptions.

    Args:
        request: The incoming HTTP request

    Returns:
    -------
        HTMLResponse: The rendered resume creation page
    """
    return templates.TemplateResponse("create.html", {"request": request})


@web_router.get(
    "/resume/{resume_id}",
    summary="View Resume",
    response_description="View a specific resume",
    response_class=HTMLResponse,
)
async def view_resume(
    request: Request,
    resume_id: str = Path(..., title="Resume ID"),
):
    """Render the detailed view of a specific resume.

    This endpoint displays the details of a specific resume, including
    optimization results, ATS score, and options to download or edit.

    Args:
        request: The incoming HTTP request
        resume_id: The ID of the resume to view

    Returns:
    -------
        HTMLResponse: The rendered resume view page
    """
    # In a complete implementation, we would fetch the resume data
    # from the API and pass it to the template
    return templates.TemplateResponse(
        "resume_view.html", {"request": request, "resume_id": resume_id}
    )


@web_router.get(
    "/resume/{resume_id}/optimize",
    summary="Optimize Resume",
    response_description="Optimize a specific resume",
    response_class=HTMLResponse,
)
async def optimize_resume_page(
    request: Request,
    resume_id: str = Path(..., title="Resume ID"),
):
    """Render the resume optimization page.

    This page allows users to optimize a specific resume with AI-powered tools
    after viewing its ATS score.

    Args:
        request: The incoming request
        resume_id: The unique identifier of the resume

    Returns:
    -------
        HTMLResponse: Rendered resume optimization page
    """
    return templates.TemplateResponse(
        "resume_optimize.html",
        {
            "request": request,
            "resume_id": resume_id,
            "page_title": "Optimize Resume",
        },
    )


@web_router.get(
    "/settings",
    summary="Settings",
    response_description="Manage your settings",
    response_class=HTMLResponse,
)
async def settings(
    request: Request,
):
    """Render the user settings page.

    This endpoint displays user profile settings, preferences,
    and account management options.

    Args:
        request: The incoming HTTP request

    Returns:
    -------
        HTMLResponse: The rendered settings page
    """
    return templates.TemplateResponse("settings.html", {"request": request})
