from fastapi import FastAPI
from redis import asyncio as aioredis
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database.connector import MongoConnectionManager
from app.api.routers.resume import resume_router
from app.web.core import core_web_router
from app.web.dashboard import web_router
from app.web.chat import chat_router

async def startup_logic(app: FastAPI) -> None:
    try:
        connection_manager = MongoConnectionManager()
        app.state.mongo = connection_manager
    except Exception as e:
        print(f"Error during startup: {e}")
        raise

async def shutdown_logic(app: FastAPI) -> None:
    try:
        await app.state.mongo.close_all()
        print("Successfully closed all database connections")
    except Exception as e:
        print(f"Error during shutdown: {e}")
    finally:
        print("Shutting down background tasks.")

app = FastAPI(
    title="MyResumo API",
    summary="",
    description=""" 
    MyResumo is an AI-backed resume generator designed to tailor your resume and skills based on a given job description. This innovative tool leverages the latest advancements in AI technology to provide you with a customized resume that stands out.
    """,
    license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
    version="2.0.0",
    docs_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/templates", StaticFiles(directory="app/templates"), name="templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    try:
        with open("app/templates/custom_swagger.html") as f:
            template = f.read()

        return HTMLResponse(
            template.replace("{{ title }}", "MyResumo API Documentation").replace(
                "{{ openapi_url }}", "/openapi.json"
            )
        )
    except FileNotFoundError:
        return HTMLResponse(
            content="Custom Swagger template not found", status_code=500
        )
    except Exception as e:
        return HTMLResponse(
            content=f"Error loading documentation: {str(e)}", status_code=500
        )


@app.get("/health", tags=["Health"], summary="Health Check")
async def health_check():
    """
    Health check endpoint for monitoring and container orchestration.
    
    Returns:
        JSONResponse: Status information about the application.
    """
    return JSONResponse(
        content={
            "status": "healthy",
            "version": app.version,
            "service": "myresumo"
        }
    )


app.include_router(resume_router)
app.include_router(core_web_router)
app.include_router(web_router)
app.include_router(chat_router)