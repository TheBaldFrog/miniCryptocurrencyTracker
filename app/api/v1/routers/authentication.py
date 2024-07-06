from fastapi import APIRouter

from app.dependencies.dependencies import DBSessionDep
from app.dto.schema.cryptocurrency import ResponseSchema
from app.dto.schema.user import ForgotPasswordSchema, LoginSchema, RegisterSchema
from app.service.authentication import AuthService

authentication_router = APIRouter(prefix="/auth", tags=["Authentication"])


@authentication_router.post(
    "/register", response_model=ResponseSchema, response_model_exclude_none=True
)
async def register(request_body: RegisterSchema, db: DBSessionDep):
    await AuthService.register_service(request_body, db)
    return ResponseSchema(detail="Successfully registered")


@authentication_router.post("/login", response_model=ResponseSchema)
async def login(request_body: LoginSchema, db: DBSessionDep):
    token = await AuthService.logins_service(request_body, db)
    return ResponseSchema(
        detail="Successfully login",
        result={"token_type": "Bearer", "access_token": token},
    )


@authentication_router.post(
    "/forgot-password", response_model=ResponseSchema, response_model_exclude_none=True
)
async def forgot_password(request_body: ForgotPasswordSchema, db: DBSessionDep):
    await AuthService.forgot_password_service(request_body, db)
    return ResponseSchema(detail="Successfully update data!")
