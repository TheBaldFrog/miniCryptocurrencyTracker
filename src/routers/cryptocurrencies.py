from fastapi import APIRouter

cryptocurrencies = APIRouter(
    prefix="/cryptocurrencies",
)


@cryptocurrencies.get("/")
async def get_cryptocurrencies():
    return await cmc_client.get_listings()


@cryptocurrencies.get("/cryptocurrencies/{currency_id}")
async def get_cryptocurrency(currency_id: int):
    return await cmc_client.get_currencies(currency_id)
