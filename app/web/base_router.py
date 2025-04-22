"""Base router module for web interface routes.

This module provides the WebRouter class, which extends FastAPI's APIRouter
to provide specialized functionality for MyResumo's web interface routes.
"""

from fastapi import APIRouter


class WebRouter(APIRouter):
    """Base router class for web interface endpoints.

    This class extends FastAPI's APIRouter to provide consistent settings
    for all web interface routes, such as tagging, templating,
    and response class configuration.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the WebRouter with consistent settings.

        Args:
            *args: Variable length argument list passed to parent APIRouter
            **kwargs: Arbitrary keyword arguments passed to parent APIRouter
        """
        super().__init__(
            tags=["Web"],
            # Additional standard settings can be added here
            **kwargs,
        )
