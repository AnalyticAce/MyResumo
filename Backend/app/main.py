import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.connector import MongoConnectionManager
from app.routers.auth.oauth2 import oauth2_router
from app.routers.api.api import user_router
from app.credentials.config import REDIS_HOST, REDIS_PORT
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

async def startup_logic(app: FastAPI) -> tuple[asyncio.Task, asyncio.Task]:
    connection_manager = MongoConnectionManager()
    app.state.mongo = connection_manager

    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

async def shutdown_logic(app: FastAPI):
    await app.state.mongo.close_all()
    print("Shutting down background tasks.")

app = FastAPI(
    title="MyResumo API Documentation",
    summary="MyResumo API Documentation",
    description="""
    MyResumo is an AI-backed resume generator designed to tailor your resume and skills based on a given job description. This innovative tool leverages the latest advancements in AI technology to provide you with a customized resume that stands out.
    """,
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    version="1.0.0",
    docs_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(oauth2_router)
app.include_router(user_router)

app.mount("/templates", StaticFiles(directory="app/templates"), name="templates")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    with open("app/templates/custom_swagger.html") as f:
        template = f.read()
    
    return HTMLResponse(
        template.replace(
            "{{ title }}", 
            "MyResumo API Documentation"
        ).replace(
            "{{ openapi_url }}", 
            "/openapi.json"
        )
    )