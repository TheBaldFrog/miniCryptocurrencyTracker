from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from src.api.v1.routers import cryptocurrencies
from src.dependencies.cmc_http_client import start_cmc_http_client, stop_cmc_http_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    logger.info("on_start_up")
    start_cmc_http_client()
    yield
    logger.info("on_shutdown")
    await stop_cmc_http_client()


app = FastAPI(title="FastAPI React App", lifespan=lifespan)
app.include_router(cryptocurrencies)


@app.get("/")
def root():
    return {"Hello": "Fastapi and React App"}
