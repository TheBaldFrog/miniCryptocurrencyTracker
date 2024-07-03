from typing import Annotated

from fastapi import APIRouter, Depends

from src.dependencies.cmc_http_client import CMSHTTPClient
from src.dependencies.dependencies import get_cmc_client

cryptocurrencies = APIRouter(prefix="/cryptocurrencies", tags=["cryptocurrencies"])


@cryptocurrencies.get("/")
async def get_cryptocurrencies(
    cmc_client: Annotated[CMSHTTPClient, Depends(get_cmc_client)]
):
    return await cmc_client.get_listings()


@cryptocurrencies.get("/{currency_id}")
async def get_cryptocurrency(
    currency_id: int, cmc_client: Annotated[CMSHTTPClient, Depends(get_cmc_client)]
):
    return await cmc_client.get_currencies(currency_id)
