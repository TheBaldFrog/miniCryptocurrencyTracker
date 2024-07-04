from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies.dependencies import get_cmc_client
from app.schemas.cryptocurrency import Cryptocurrency
from app.services.coinmarketcap.cmc_http_client import CMSHTTPClient

cryptocurrencies = APIRouter(prefix="/cryptocurrencies", tags=["Cryptocurrencies"])


@cryptocurrencies.get("/")
async def get_cryptocurrencies(
    cmc_client: Annotated[CMSHTTPClient, Depends(get_cmc_client)]
) -> list[Cryptocurrency]:
    return await cmc_client.get_listings()


@cryptocurrencies.get("/{currency_id}")
async def get_cryptocurrency(
    currency_id: int, cmc_client: Annotated[CMSHTTPClient, Depends(get_cmc_client)]
) -> Cryptocurrency:
    return await cmc_client.get_currencies(currency_id)
