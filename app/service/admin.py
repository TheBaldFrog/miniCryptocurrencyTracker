from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.schema.cryptocurrency import ResponseSchema
from app.repository.user import UserRepository
from app.service.user import UserService


class AdminService:
    @staticmethod
    async def delete_user(db: AsyncSession, admin_username: str, username: str):
        if not await UserService.is_admin(db, admin_username):
            raise HTTPException(status_code=403, detail="Not enough permissions")

        user = await UserRepository.get_by_username(db, username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        try:
            await UserRepository.delete(db, user)
            return ResponseSchema(
                detail=f"Successfully delete user with username:{username}"
            )
        except Exception:
            raise HTTPException(status_code=404, detail=f"Model:{username} not found")

    @staticmethod
    async def update_privileges(
        db: AsyncSession, admin_username: str, username: str, admin: bool
    ):
        if not await UserService.is_admin(db, admin_username):
            raise HTTPException(status_code=403, detail="Not enough permissions")

        user = await UserRepository.get_by_username(db, username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        user.is_superuser = admin

        await UserRepository.update(db, user)

        return ResponseSchema(
            detail=f"Successfully changed privileges for user:{username} - admin:{user.is_superuser}"
        )
