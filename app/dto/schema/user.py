import re
from enum import Enum

from fastapi import HTTPException
from pydantic import BaseModel, field_validator


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_superuser: bool = False


class UserPrivateSchema(UserSchema):
    hashed_password: str


class Sex(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class RegisterSchema(BaseModel):

    username: str
    email: str
    name: str
    password: str
    phone_number: str
    birth: str
    sex: Sex

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


# schema = RegisterSchema(
#     username="dsf",
#     email="<EMAIL>",
#     name="dsad",
#     password="dsa",
#     phone_number="+393515777020",
#     birth="fsdf",
#     sex="FEMALE",
# )
