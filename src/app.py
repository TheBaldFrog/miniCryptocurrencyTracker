from fastapi import FastAPI
from fastapi.logger import logger as fastapi_logger

from src.api.v1.routers import cryptocurrencies
from src.dependencies.cmc_http_client import start_cmc_http_client, stop_cmc_http_client


async def on_start_up() -> None:
    fastapi_logger.info("on_start_up")

    start_cmc_http_client()


async def on_shutdown() -> None:
    fastapi_logger.info("on_shutdown")

    await stop_cmc_http_client()


app = FastAPI(
    on_startup=[on_start_up], on_shutdown=[on_shutdown], title="FastAPI React App"
)
app.include_router(cryptocurrencies)


@app.get("/")
def root():
    return {"Hello": "Fastapi and React App"}
