from datetime import datetime

import phonenumbers
from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.dependencies import pwd_context
from app.dto.model import User
from app.dto.schema.user import ForgotPasswordSchema, LoginSchema, RegisterSchema
from app.repository.jwt import JWTRepo
from app.repository.user import UserRepository


class AuthService:
    @staticmethod
    async def register_service(register: RegisterSchema, db: AsyncSession):
        # Validate email
        try:
            email_info = validate_email(register.email, check_deliverability=False)

            normalized_email = email_info.normalized
        except EmailNotValidError:
            raise HTTPException(status_code=400, detail="Non valid email!")

        # Validate phonenumbers
        my_number = phonenumbers.parse(register.phone_number)
        if not phonenumbers.is_valid_number(my_number):
            raise HTTPException(status_code=400, detail="Non valid phone number!")

        # Validate birthdate type from frontend str to date
        try:
            birth_date = datetime.strptime(register.birth, "%d-%m-%Y")
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid birth, date does not match format '%d-%m-%Y'",
            )

        _users = User(
            username=register.username,
            email=normalized_email,
            hashed_password=pwd_context.hash(register.password),
            birth=birth_date,
            first_name=register.first_name,
            last_name=register.last_name,
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
        raise HTTPException(status_code=400, detail="Username not found!")

    @staticmethod
    async def forgot_password_service(
        forgot_password: ForgotPasswordSchema, db: AsyncSession
    ):
        _user = await UserRepository.get_by_email(db, forgot_password.email)

        if _user is None:
            raise HTTPException(status_code=400, detail="Email not found!")

        if pwd_context.verify(forgot_password.new_password, _user.hashed_password):
            raise HTTPException(
                status_code=400, detail="The new password is the same as the old one!"
            )

        new_hashed_password = pwd_context.hash(forgot_password.new_password)
        _user.hashed_password = new_hashed_password

        await UserRepository.update(db, _user)
