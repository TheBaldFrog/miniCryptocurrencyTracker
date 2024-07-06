from typing import Annotated

from fastapi import Depends
from loguru import logger
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_db_manager
from app.service.coinmarketcap.cmc_http_client import (
    CMSHTTPClient,
    CMSHTTPClientSingletonWrapper,
)


# Coinmarketcap
def get_cmc_client() -> CMSHTTPClient:
    return CMSHTTPClientSingletonWrapper.get_instance()


async def get_db():
    db = async_db_manager.get_new_session()
    logger.debug("Open async session")
    try:
        yield db
    finally:
        await db.close()
        logger.debug("Close async session")


DBSessionDep = Annotated[AsyncSession, Depends(get_db)]


async def commit_rollback(db: AsyncSession):
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def asdict(obj):
#     return dict(
#         (col.name, getattr(obj, col.name))
#         for col in class_mapper(obj.__class__).mapped_table.c
#     )
