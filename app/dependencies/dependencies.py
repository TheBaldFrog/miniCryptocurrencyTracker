from loguru import logger

from app.core.database import async_db_manager
from app.service.coinmarketcap.cmc_http_client import (
    CMSHTTPClient,
    CMSHTTPClientSingletonWrapper,
)


# Coinmarketcap
def get_cmc_client() -> CMSHTTPClient:
    return CMSHTTPClientSingletonWrapper.get_instance()


async def get_db():
    db = async_db_manager.get_session()
    logger.debug("Open async session")
    try:
        yield db
    finally:
        await db.close()
        logger.debug("Close async session")
