from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.v1.routers import (
    admin_router,
    authentication_router,
    cryptocurrencies,
    user_router,
)
from app.core.config import config
from app.core.database import async_db_manager
from app.service.coinmarketcap.cmc_http_client import (
    start_cmc_http_client,
    stop_cmc_http_client,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Up
    logger.info("on_start_up")

    await async_db_manager.init()
    logger.debug("start DB")

    start_cmc_http_client()
    logger.debug("start_cmc_http_client")
    yield
    # Shutdown
    logger.info("on_shutdown")

    await stop_cmc_http_client()
    logger.debug("stop_cmc_http_client")

    if not async_db_manager.is_closed():
        await async_db_manager.close()
        logger.debug("Close the DB connection")


app = FastAPI(title=config.project_name, lifespan=lifespan)
app.include_router(cryptocurrencies)
app.include_router(authentication_router)
app.include_router(user_router)
app.include_router(admin_router)


origins = ["http://localhost", f"http://localhost:{config.vite_port}", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"Title": config.project_name}
