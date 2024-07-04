from async_lru import alru_cache
from loguru import logger

from app.core.config import config
from app.service.coinmarketcap.http_client import HTTPClient


class CMSHTTPClient(HTTPClient):
    @alru_cache(maxsize=32)
    async def get_listings(self):
        async with self._session.get("/v1/cryptocurrency/listings/latest") as resp:
            result = await resp.json()
            return result["data"]

    @alru_cache(maxsize=32)
    async def get_currencies(self, currency_id: int):
        async with self._session.get(
            "/v2/cryptocurrency/quotes/latest", params={"id": currency_id}
        ) as resp:
            result = await resp.json()
            return result["data"][str(currency_id)]


class CMSHTTPClientSingletonWrapper:
    _instance: CMSHTTPClient = None

    @classmethod
    def get_instance(cls) -> CMSHTTPClient:
        if cls._instance is None:
            logger.error("No CMSHTTPClient initialized")

        return cls._instance

    @classmethod
    def init_instance(cls, cmc_client: CMSHTTPClient):
        cls._instance = cmc_client


def start_cmc_http_client():
    CMSHTTPClientSingletonWrapper.init_instance(
        CMSHTTPClient(
            base_url=config.cmc_http_client.base_url,
            api_key=config.cmc_http_client.cmc_api_key,
        )
    )


async def stop_cmc_http_client():
    await CMSHTTPClientSingletonWrapper.get_instance().close_session()
