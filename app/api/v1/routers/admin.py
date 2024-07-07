from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials

from app.dependencies.dependencies import DBSessionDep
from app.dto.schema.cryptocurrency import ResponseSchema
from app.repository.jwt import JWTBearer, JWTRepo
from app.service.admin import AdminService

admin_router = APIRouter(prefix="/admin", tags=["Admin"])


@admin_router.delete(
    "/delete-user/{username}",
    response_model_exclude_none=True,
)
async def delete_user_by_id(
    username: str,
    db: DBSessionDep,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer()),
) -> ResponseSchema:
    token = JWTRepo.extract_token(str(credentials))
    return await AdminService.delete_user(db, token["username"], username)
