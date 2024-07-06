from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.sync import update

from app.dto.model import User
from app.repository.base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User:
        query = select(User).where(User.email == email)
        return (await db.execute(query)).scalar_one_or_none()

    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> User:
        query = select(User).where(User.username == username)
        return (await db.execute(query)).scalar_one_or_none()

    # @staticmethod
    # async def update_password(self, db: AsyncSession, email: str, password: str):
    #     query = update(User).where(User.email == email).values(
    #         password=password).execution_options(synchronize_session="fetch")
    #     await db.execute(query)
    #
    #     try:
    #         await db.commit()
    #     except Exception:
    #         await db.rollback()
    #         raise
