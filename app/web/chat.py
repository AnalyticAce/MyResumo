from fastapi import APIRouter, HTTPException, Request, status
from app.web.base_router import WebRouter
from fastapi.templating import Jinja2Templates

chat_router = WebRouter()
templates = Jinja2Templates(directory="templates")

@chat_router.get(
    "/chat",
    summary="Chat",
    response_description="Chat with MyResumo",
)
async def chat(
    request: Request,
):
    pass
