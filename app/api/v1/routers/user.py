from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials

from app.dependencies.dependencies import DBSessionDep, get_db
from app.dto.schema.cryptocurrency import ResponseSchema
from app.dto.schema.user import (
    RegisterSchema,
    UpdatePasswordSchema,
    UpdateUserSchema,
    UserProfileSchema,
    UserPublicSchema,
)
from app.repository.jwt import JWTBearer, JWTRepo
from app.repository.user import UserRepository
from app.service.user import UserService

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.get("/", response_model=list[UserPublicSchema])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db=Depends(get_db),
):
    all_users = await UserRepository.get_all(db, skip, limit)
    return all_users


@user_router.get("/id/{user_id}")
async def get_by_id(
    user_id: int,
    db: DBSessionDep,
) -> UserPublicSchema:
    user = await UserRepository.get_by_id(db, user_id)
    if user is not None:
        return user
    raise HTTPException(status_code=404, detail=f"User:{user_id} not found")


@user_router.get("/profile", response_model=UserProfileSchema)
async def get_current_user_profile(
    db: DBSessionDep, credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    token = JWTRepo.extract_token(str(credentials))
    user = await UserService.get_user_profile(db, token["username"])
    return user


@user_router.get("/email/{email}", response_model=UserPublicSchema)
async def get_user_by_email(
    email: str,
    db: DBSessionDep,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer()),
):
    user = await UserRepository.get_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail=f"email:{email} not found")
    return user


@user_router.get("/username/{username}", response_model=UserPublicSchema)
async def get_user_by_username(
    username: str,
    db: DBSessionDep,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer()),
):
    user = await UserRepository.get_by_username(db, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"username:{username} not found",
        )
    return user


@user_router.put(
    "/update", response_model=ResponseSchema, response_model_exclude_none=True
)
async def update_current_user(
    request_body: UpdateUserSchema,
    db: DBSessionDep,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer()),
):
    token = JWTRepo.extract_token(str(credentials))
    await UserService.update_profile(request_body, db, token["username"])

    return ResponseSchema(detail="Successfully update data!")


@user_router.put(
    "/update-password", response_model=ResponseSchema, response_model_exclude_none=True
)
async def update_current_user_password(
    request_body: UpdatePasswordSchema,
    db: DBSessionDep,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer()),
):
    token = JWTRepo.extract_token(str(credentials))
    await UserService.update_password(request_body, db, token["username"])

    return ResponseSchema(detail="Successfully update password!")
