import datetime
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import config


class JWTRepo:
    def __init__(self, data: dict = {}, token: str = None):
        self.data = data
        self.token = token

    def generate_token(self, expires_delta: timedelta | None = None):
        to_encode = self.data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            payload=to_encode,
            key=config.authentication.SECRET_KEY,
            algorithm=config.authentication.ALGORITHM,
        )

        return encoded_jwt

    def decode_token(self):
        try:
            decoded_token = jwt.decode(
                token=self.token,
                key=config.authentication.SECRET_KEY,
                algorithms=[config.authentication.ALGORITHM],
            )
            return decoded_token if decoded_token["expires"] >= datetime.time() else None
        except:
            return {}

    @staticmethod
    def extract_token(token: str):
        return jwt.decode(
            token=token,
            key=config.authentication.SECRET_KEY,
            algorithms=[config.authentication.ALGORITHM],
        )


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403,
                    detail={
                        "status": "Forbidden",
                        "message": "Invalid authentication schema.",
                    },
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403,
                    detail={
                        "status": "Forbidden",
                        "message": "Invalid token or expired token.",
                    },
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403,
                detail={"status": "Forbidden", "message": "Invalid authorization code."},
            )

    @staticmethod
    def verify_jwt(jwt_token: str):
        return (
            True
            if jwt.decode(
                jwt_token,
                config.authentication.SECRET_KEY,
                algorithms=[config.authentication.ALGORITHM],
            )
            is not None
            else False
        )
