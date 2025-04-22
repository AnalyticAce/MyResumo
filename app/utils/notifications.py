"""Notifications utility module for MyResumo.

This module provides helper functions for creating and managing notifications,
including toast messages for the frontend.
"""
from typing import Any, Dict, Literal

from starlette.responses import HTMLResponse, JSONResponse
from starlette.responses import Response as StarletteResponse

NotificationType = Literal["success", "error", "warning", "info"]


def create_toast_data(
    message: str,
    type: NotificationType = "info",
    duration: int = 5000,
) -> Dict[str, Any]:
    """Create toast notification data.

    Args:
        message: The text message to display in the toast notification.
        type: The type of notification (success, error, warning, or info).
        duration: The duration in milliseconds for the toast to be displayed.

    Returns:
    -------
        A dictionary with the toast notification data.
    """
    return {
        "message": message,
        "type": type,
        "duration": duration
    }


def inject_toast_script(
    response: StarletteResponse,
    message: str,
    type: NotificationType = "info",
    duration: int = 5000
) -> StarletteResponse:
    """Inject a toast notification script into an HTML response.

    This function adds a script tag to show a toast notification when the page loads.
    It should only be used for HTML responses.

    Args:
        response: The response object to modify.
        message: The text message to display in the toast.
        type: The type of notification (success, error, warning, or info).
        duration: The duration in milliseconds for the toast to be displayed.

    Returns:
    -------
        The modified response with the toast script injected.
    """
    if not isinstance(response, HTMLResponse):
        return response
    
    # Extract the content as a string
    content = response.body.decode("utf-8")
    
    # Create the script to show the toast
    script = f"""
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            if (window.showToast) {{
                window.showToast("{message}", "{type}", {duration});
            }}
        }});
    </script>
    """
    
    # Insert the script before the closing </body> tag
    if "</body>" in content:
        modified_content = content.replace("</body>", f"{script}</body>")
        response.body = modified_content.encode("utf-8")
    
    return response


def add_toast_header(
    response: StarletteResponse,
    message: str,
    type: NotificationType = "info",
    duration: int = 5000
) -> StarletteResponse:
    """Add a toast notification header to a response.
    
    This allows the client-side JavaScript to read the header and display a toast.
    Useful for API responses that redirect to HTML pages.

    Args:
        response: The response object to modify.
        message: The text message to display in the toast.
        type: The type of notification (success, error, warning, or info).
        duration: The duration in milliseconds for the toast to be displayed.

    Returns:
    -------
        The modified response with the toast header added.
    """
    response.headers["X-Toast-Message"] = message
    response.headers["X-Toast-Type"] = type
    response.headers["X-Toast-Duration"] = str(duration)
    return response


def create_response_with_toast(
    content: Dict[str, Any],
    status_code: int = 200,
    message: str = None,
    toast_type: NotificationType = "success",
    duration: int = 5000,
    headers: Dict[str, str] = None
) -> JSONResponse:
    """Create a JSON response with toast notification headers.

    Args:
        content: The content of the JSON response.
        status_code: HTTP status code.
        message: The toast message to display. If None, no toast will be added.
        toast_type: The type of toast notification.
        duration: The duration in milliseconds for the toast to be displayed.
        headers: Additional headers to add to the response.

    Returns:
    -------
        A JSONResponse with toast notification headers if a message was provided.
    """
    headers = headers or {}
    
    if message:
        headers.update({
            "X-Toast-Message": message,
            "X-Toast-Type": toast_type,
            "X-Toast-Duration": str(duration)
        })
    
    return JSONResponse(
        content=content,
        status_code=status_code,
        headers=headers
    )