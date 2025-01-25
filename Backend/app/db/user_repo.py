from typing import Optional, Dict, List
from bson import ObjectId
from app.db.base_repo import BaseRepository
from app.routers.models import UserInDB

class UserRepository(BaseRepository):
    def __init__(self, db_name: str):
        super().__init__(db_name, "users")

    async def get_user(self, full_name: str) -> Optional[UserInDB]:
        user = await self.find_one({"full_name": full_name})
        if user:
            return UserInDB(**self._map_user_data(user))
        return None

    async def create_user(self, user_data: Dict) -> UserInDB:
        user_id = await self.insert_one(user_data)
        created_user = await self.find_one({"_id": ObjectId(user_id)})
        return UserInDB(**self._map_user_data(created_user))

    async def update_user(self, full_name: str, update_data: Dict) -> bool:
        return await self.update_one({"full_name": full_name}, update_data)

    async def delete_user(self, full_name: str) -> bool:
        return await self.delete_one({"full_name": full_name})

    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        user = await self.find_one({"email": email})
        if user:
            return UserInDB(**self._map_user_data(user))
        return None

    def _map_user_data(self, user_data: Dict) -> Dict:
        return {
            "full_name": user_data.get("full_name"),
            "email": user_data.get("email"),
            "hashed_password": user_data.get("hashed_password", ""),
            "provider": user_data.get("provider", "createk"),
            "disabled": user_data.get("disabled", False),
            "profile_picture": user_data.get("profile_picture", None),
            "following": user_data.get("following", []),
            "followers": user_data.get("followers", []),
            "social_links": user_data.get("social_links", {})
        }