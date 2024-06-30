from fastapi import FastAPI

from src.config import Settings
from src.dependencies.http_client import CMSHTTPClient

cmc_client = CMSHTTPClient(
    base_url="https://pro-api.coinmarketcap.com", api_key=Settings.CMC_API_KEY
)


app = FastAPI()


@app.get("/")
def root():
    return {"Hello fdd": "vds"}
