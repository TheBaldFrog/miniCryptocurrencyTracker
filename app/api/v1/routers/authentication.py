import datetime

from fastapi import APIRouter, HTTPException
from loguru import logger

from app.dependencies.dependencies import DBSessionDep
from app.dto.model import User
from app.dto.schema.cryptocurrency import ResponseSchema
from app.dto.schema.user import RegisterSchema
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
async def register(request_body: RegisterSchema, db: DBSessionDep):
    user = User(
        username=request_body.username,
        email=request_body.email,
        first_name=request_body.name,
        last_name=request_body.name,
        hashed_password=f"fsdfsddsfsdfsdfd+ {request_body.password}",
        phone_number=request_body.phone_number,
        sex=request_body.sex,
        birth=datetime.date(1902, 1, 1),
    )
    try:
        model = await UserRepository.create(db=db, orm_model=user)
        logger.debug(model.email)
    except Exception:
        raise HTTPException(status_code=404, detail=f"User already exists")
    return ResponseSchema(detail="Successfully save data!")


@authentication_router.get("/Users")
async def get_users(db: DBSessionDep):
    all_users = await UserRepository.get_all(db)
    print(len(all_users))
    return {"data": all_users}


@authentication_router.get("/user/{user_id}")
async def get_by_id(user_id: int, db: DBSessionDep):
    user = await UserRepository.get_by_id(db, user_id)
    if user is not None:
        return {"user": user}
    raise HTTPException(status_code=404, detail=f"Model:{user_id} not found")


@authentication_router.get("/updateUser")
async def update_user(db: DBSessionDep):
    user = await UserRepository.get_by_id(db, 7)
    user.username = "new Username7"
    user.email = "newemail7"
    await UserRepository.update(db, user)
    return {"id": user}


@authentication_router.get("/deleteUser/{user_id}")
async def delete_user_by_id(user_id: int, db: DBSessionDep):
    try:
        await UserRepository.delete_by_id(db, user_id)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Model:{user_id} not found")


@authentication_router.get("/deleteUser")
async def delete_user(db: DBSessionDep):
    user = await UserRepository.get_by_id(db, 4)

    if user is None:
        raise HTTPException(status_code=404, detail=f"Model:4 not found")

    try:
        await UserRepository.delete(db, user)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Error delete user")


@authentication_router.get("/user/getEmail/{email}")
async def get_by_email(email: str, db: DBSessionDep):
    user = await UserRepository.get_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail=f"Model:{email} not found")
    return {"user": user}


@authentication_router.get("user/getUsername/{username}")
async def get_by_username(username: str, db: DBSessionDep):
    user = await UserRepository.get_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail=f"Model:{username} not found")
    return {"user": user}
