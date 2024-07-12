import re
from datetime import date, datetime
from enum import Enum

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator


class Sex(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class RegisterSchema(BaseModel):

    username: str
    email: str = Field(default="user@mail.com")
    first_name: str
    last_name: str
    password: str
    phone_number: str
    birth: str = Field(default="01-01-2001")
    sex: Sex

    @field_validator("username")
    def validate_username(cls, v):
        return v.strip()

    @field_validator("email")
    def validate_email(cls, v):
        return v.strip()

    @field_validator("password")
    def validate_password(cls, v):
        return v.strip()

    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        return v.strip()

    @field_validator("birth")
    def validate_birth(cls, v):
        return v.strip()

    @field_validator("sex")
    def sex_validation(cls, v):
        if hasattr(Sex, v) is False:
            raise HTTPException(status_code=400, detail="Invalid input sex")
        return v

    @field_validator("phone_number")
    def phone_validation(cls, v):
        # regex phone number
        regex = r"^[\+]?[(]?[0-9]{4}[)]?[-\s\.]?[0-9]{4}[-\s\.]?[0-9]{4,6}$"
        if v and not re.search(regex, v, re.I):
            raise HTTPException(status_code=400, detail="Invalid input phone number!")
        return v


class LoginSchema(BaseModel):
    username: str
    password: str


class ForgotPasswordSchema(BaseModel):
    email: str
    new_password: str


class UserProfileSchema(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    phone_number: str
    birth: datetime | str
    sex: str
    is_superuser: bool = False


class UserPublicSchema(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    sex: str
    is_superuser: bool


class UpdateUserSchema(BaseModel):
    username: str
    email: str = Field(default="user@mail.com")
    first_name: str
    last_name: str
    phone_number: str
    birth: str = Field(default="01-01-2001", title="%d-%m-%Y")
    sex: Sex

    @field_validator("username")
    def validate_username(cls, v):
        return v.strip()

    @field_validator("email")
    def validate_email(cls, v):
        return v.strip()

    @field_validator("first_name")
    def validate_first_name(cls, v):
        return v.strip()

    @field_validator("last_name")
    def validate_last_name(cls, v):
        return v.strip()

    @field_validator("phone_number")
    def phone_validation(cls, v):
        # regex phone number
        regex = r"^[\+]?[(]?[0-9]{4}[)]?[-\s\.]?[0-9]{4}[-\s\.]?[0-9]{4,6}$"
        if v and not re.search(regex, v, re.I):
            raise HTTPException(status_code=400, detail="Invalid input phone number!")
        return v


class UpdatePasswordSchema(BaseModel):
    old_password: str
    new_password: str


class UpdatePrivilegesUserSchema(BaseModel):
    username: str
    is_superuser: bool
