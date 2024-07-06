from fastapi import APIRouter, HTTPException

from app.dependencies.dependencies import DBSessionDep
from app.repository.user import UserRepository

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.get("")
async def get_users(db: DBSessionDep):
    all_users = await UserRepository.get_all(db)
    print(len(all_users))
    return {"data": all_users}


@user_router.get("/{user_id}")
async def get_by_id(user_id: int, db: DBSessionDep):
    user = await UserRepository.get_by_id(db, user_id)
    if user is not None:
        return {"user": user}
    raise HTTPException(status_code=404, detail=f"Model:{user_id} not found")


# TEST FUNCTIONS
@user_router.get("/update")
async def update_user(db: DBSessionDep):
    user = await UserRepository.get_by_id(db, 7)
    user.username = "new Username7"
    user.email = "newemail7"
    await UserRepository.update(db, user)
    return {"id": user}


@user_router.get("/delete/{user_id}")
async def delete_user_by_id(user_id: int, db: DBSessionDep):
    try:
        await UserRepository.delete_by_id(db, user_id)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Model:{user_id} not found")


@user_router.get("/deleteUser")
async def delete_user(db: DBSessionDep):
    user = await UserRepository.get_by_id(db, 4)

    if user is None:
        raise HTTPException(status_code=404, detail=f"Model:4 not found")

    try:
        await UserRepository.delete(db, user)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Error delete user")


@user_router.get("/user/getEmail/{email}")
async def get_by_email(email: str, db: DBSessionDep):
    user = await UserRepository.get_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail=f"Model:{email} not found")
    return {"user": user}


@user_router.get("user/getUsername/{username}")
async def get_by_username(username: str, db: DBSessionDep):
    user = await UserRepository.get_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail=f"Model:{username} not found")
    return {"user": user}
