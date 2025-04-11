from fastapi import FastAPI
from redis import asyncio as aioredis
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database.connector import MongoConnectionManager
from app.core.config import REDIS_HOST, REDIS_PORT


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

@app.get("/upload/{filename}")
async def upload_file(filename: str):
    return {"filename": filename}

# @app.get("/chat")
# async def chat():
#     return {"message": "Hello World"}

# @app.get("/chat/{chat_id}")
# async def chat(chat_id: str):
#     return {"message": f"Hello {chat_id}"}

# @app.get("/settings")
# async def settings():
#     return {"message": "Hello World"}

