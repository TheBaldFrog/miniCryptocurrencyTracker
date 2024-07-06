import datetime

from fastapi import APIRouter, HTTPException
from loguru import logger
from sqlalchemy.orm import class_mapper

from app.dependencies.dependencies import DBSessionDep
from app.dto.model import User
from app.dto.schema.cryptocurrency import ResponseSchema
from app.repository.user import UserRepository

authentication_router = APIRouter(prefix="/auth", tags=["Authentication"])


# def asdict(obj):
#     return dict(
#         (col.name, getattr(obj, col.name))
#         for col in class_mapper(obj.__class__).mapped_table.c
#     )


@authentication_router.post(
    "/register", response_model=ResponseSchema, response_model_exclude_none=True
)
async def register(db: DBSessionDep):
    user_repo = UserRepository()
    user = User(
        username="55",
        email="55",
        first_name="1",
        last_name="2",
        hashed_password="fsdfsddsfsdfsdfd",
        phone_number="+393515777020",
        sex="MALE",
        birth=datetime.date(1902, 1, 1),
    )
    try:
        model = await user_repo.create(db=db, orm_model=user)
        logger.debug(model.email)
    except Exception:
        raise HTTPException(status_code=404, detail=f"User already exists")
    return ResponseSchema(detail="Successfully save data!")


@authentication_router.get("/Users")
async def get_users(db: DBSessionDep):
    base_repo = UserRepository()
    all_users = await base_repo.get_all(db)
    print(len(all_users))
    return {"data": all_users}


@authentication_router.get("/user/{user_id}")
async def get_by_id(user_id: int, db: DBSessionDep):
    user_repo = UserRepository()

    user = await user_repo.get_by_id(db, user_id)
    if user is not None:
        return {"user": user}
    raise HTTPException(status_code=404, detail=f"Model:{user_id} not found")


@authentication_router.get("/updateUser")
async def update_user(db: DBSessionDep):
    base_repo = UserRepository()

    user = await base_repo.get_by_id(db, 13)
    user.username = "new Username13"
    user.email = "new email13"
    await base_repo.update(db, user)
    return {"id": user}


@authentication_router.get("/deleteUser/{user_id}")
async def delete_user_by_id(user_id: int, db: DBSessionDep):
    user_repo = UserRepository()
    try:
        await user_repo.delete_by_id(db, user_id)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Model:{user_id} not found")


@authentication_router.get("/deleteUser")
async def delete_user(db: DBSessionDep):
    user_repo = UserRepository()
    user = await user_repo.get_by_id(db, 14)

    if user is None:
        raise HTTPException(status_code=404, detail=f"Model:12 not found")

    try:
        await user_repo.delete(db, user)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Error delete user")
