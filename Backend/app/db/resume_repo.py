from typing import Optional, Dict, List
from bson import ObjectId
from app.db.base_repo import BaseRepository
from app.routers.models import UserInDB

class ResumeRepository(BaseRepository):
    def __init__(self, db_name: str):
        super().__init__(db_name, "resumes")