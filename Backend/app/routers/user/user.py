from fastapi import APIRouter, Depends, HTTPException
from app.db.user_repo import UserRepository
from app.routers.models import User, UserInDB
from app.utils.auth_utils import get_current_active_user

user_router = APIRouter(
    prefix="/api/v1/users",
    tags=["User Management"],
    responses={
        404: {"description": "Endpoint not found"},
        403: {"description": "Forbidden access"},
        200: {"description": "Success response"},
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized access"},
        409: {"description": "username already exists"},
    }
)

user_repo = UserRepository("myresumo")

@user_router.get("/me", response_model=User)
async def read_users_me(current_user: UserInDB = Depends(get_current_active_user)):
    try:
        user = await user_repo.find_one({"username": current_user.username})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.get("/me/id", response_model=str)
async def get_me_id(current_user: UserInDB = Depends(get_current_active_user)):
    try:
        user = await user_repo.find_one({"username": current_user.username})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user["id"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.delete("/me", status_code=204)
async def delete_user(current_user: UserInDB = Depends(get_current_active_user)):
    try:
        if not await user_repo.delete_user(current_user.username):
            raise HTTPException(status_code=500, detail="Failed to delete user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))