from fastapi import APIRouter, Depends, HTTPException
from app.db.user_repo import UserRepository
from app.routers.models import User, UserInDB
from app.utils.auth_utils import get_current_active_user

user_router = APIRouter(
    prefix="/api/users",
    tags=["User Management"]
)

user_repo = UserRepository("createk")

@user_router.get("/me", response_model=User)
async def read_users_me(current_user: UserInDB = Depends(get_current_active_user)):
    return current_user

@user_router.get("/me/id", response_model=str)
async def get_me_id(current_user: UserInDB = Depends(get_current_active_user)):
    user = await user_repo.find_one({"full_name": current_user.full_name})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user["id"]

@user_router.delete("/me", status_code=204)
async def delete_user(current_user: UserInDB = Depends(get_current_active_user)):
    if not await user_repo.delete_user(current_user.full_name):
        raise HTTPException(status_code=500, detail="Failed to delete user")