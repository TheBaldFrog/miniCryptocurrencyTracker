from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.dependencies import pwd_context
from app.dto.schema.user import UpdatePasswordSchema, UpdateUserSchema
from app.repository.user import UserRepository
from app.service.authentication import AuthService


class UserService:
    @staticmethod
    async def get_user_profile(db: AsyncSession, username: str):
        _user = await UserRepository.get_by_username(db, username)

        if _user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return _user

    @staticmethod
    async def update_profile(
        user_to_update: UpdateUserSchema, db: AsyncSession, username: str
    ):
        user = await UserRepository.get_by_username(db, username)

        # Checking the same username
        _username = await UserRepository.get_by_username(db, user_to_update.username)
        if _username:
            raise HTTPException(status_code=400, detail="Username already exists!")

        # Checking the same email
        _email = await UserRepository.get_by_email(db, user_to_update.email)
        if _email:
            raise HTTPException(status_code=400, detail="Email already exists!")

        AuthService.validate_phone_number(user_to_update.phone_number)

        # update
        normalized_new_email = AuthService.validate_email(user_to_update.email)
        new_birth_date = AuthService.validate_birthday(user_to_update.birth)

        user.username = user_to_update.username
        user.email = normalized_new_email
        user.first_name = user_to_update.first_name
        user.last_name = user_to_update.last_name
        user.birth = new_birth_date
        user.sex = user_to_update.sex
        user.phone_number = user_to_update.phone_number

        await UserRepository.update(db, user)

    @staticmethod
    async def update_password(
        password_schema: UpdatePasswordSchema, db: AsyncSession, username: str
    ):
        _user = await UserRepository.get_by_username(db, username)

        if not pwd_context.verify(password_schema.old_password, _user.hashed_password):
            raise HTTPException(
                status_code=400, detail="Incorrect old password! Please try again."
            )

        if password_schema.old_password == password_schema.new_password:
            raise HTTPException(
                status_code=400, detail="The new password is the same as old password!"
            )

        new_hashed_password = pwd_context.hash(password_schema.new_password)
        _user.hashed_password = new_hashed_password

        await UserRepository.update(db, _user)

    @staticmethod
    async def is_admin(db: AsyncSession, username: str) -> bool:
        user = await UserRepository.get_by_username(db, username)
        if user is None:
            return False

        return True if user.is_superuser else False
