from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.api.v1.routers import cryptocurrencies
from src.core.config import config
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


origins = [
    "http://localhost",
    f"http://localhost:{config.vite_port}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"Hello": "Fastapi and React App"}
