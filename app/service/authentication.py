from datetime import datetime

from fastapi import HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.dependencies import pwd_context
from app.dto.model import User
from app.dto.schema.user import ForgotPasswordSchema, LoginSchema, RegisterSchema
from app.repository.jwt import JWTRepo
from app.repository.user import UserRepository


class AuthService:
    @staticmethod
    async def register_service(register: RegisterSchema, db: AsyncSession):
        # convert birthdate type from frontend str to date
        birth_date = datetime.strptime(register.birth, "%d-%m-%Y")
        name = register.name.strip().split()
        first_name = name[0]
        last_name = name[1]

        _users = User(
            username=register.username,
            email=register.email,
            hashed_password=pwd_context.hash(register.password),
            birth=birth_date,
            first_name=first_name,
            last_name=last_name,
            phone_number=register.phone_number,
            sex=register.sex,
        )

        # Checking the same username
        _username = await UserRepository.get_by_username(db, register.username)
        if _username:
            raise HTTPException(status_code=400, detail="Username already exists!")

        # Checking the same email
        _email = await UserRepository.get_by_email(db, register.email)
        if _email:
            raise HTTPException(status_code=400, detail="Email already exists!")

        await UserRepository.create(db, _users)

    @staticmethod
    async def logins_service(login: LoginSchema, db: AsyncSession):
        _username = await UserRepository.get_by_username(db, login.username)

        if _username is not None:
            if not pwd_context.verify(login.password, _username.hashed_password):
                raise HTTPException(
                    status_code=400, detail="Incorrect username or password!"
                )
            return JWTRepo(data={"username": _username.username}).generate_token()
        raise HTTPException(status_code=400, detail="Username not found !")

    @staticmethod
    async def forgot_password_service(
        forgot_password: ForgotPasswordSchema, db: AsyncSession
    ):
        _user = await UserRepository.get_by_email(db, forgot_password.email)

        if _user is None:
            raise HTTPException(status_code=400, detail="Email not found !")

        if pwd_context.verify(forgot_password.new_password, _user.hashed_password):
            raise HTTPException(
                status_code=400, detail="The new password is the same as the old one"
            )

        new_hashed_password = pwd_context.hash(forgot_password.new_password)
        _user.hashed_password = new_hashed_password

        await UserRepository.update(db, _user)
