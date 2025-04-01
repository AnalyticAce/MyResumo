import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY") or None
if SECRET_KEY is None:
    raise ValueError("No SECRET_KEY set for FastAPI application")

ALGORITHM = os.environ.get("ALGORITHM")
if ALGORITHM is None:
    raise ValueError("No ALGORITHM set for FastAPI application")

ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
if ACCESS_TOKEN_EXPIRE_MINUTES is None:
    raise ValueError("No ACCESS_TOKEN_EXPIRE_MINUTES set for FastAPI application")

MONGO_CONNECTION_STRING = os.environ.get("MONGO_CONNECTION_STRING")
if MONGO_CONNECTION_STRING is None:
    raise ValueError("No MONGO_CONNECTION_STRING set for FastAPI application")

REDIS_HOST = os.environ.get("REDIS_HOST")
if REDIS_HOST is None:
    raise ValueError("No REDIS_HOST set for FastAPI application")

REDIS_PORT = os.environ.get("REDIS_PORT")
if REDIS_PORT is None:
    raise ValueError("No REDIS_PORT set for FastAPI application")

SERVER_HOST = os.environ.get("SERVER_HOST")
if SERVER_HOST is None:
    raise ValueError("No SERVER_HOST set for FastAPI application")

APP_PORT = os.environ.get("APP_PORT")
if APP_PORT is None:
    raise ValueError("No APP_PORT set for FastAPI application")