from app.services.coinmarketcap.cmc_http_client import (
    CMSHTTPClient,
    CMSHTTPClientSingletonWrapper,
)


def get_cmc_client() -> CMSHTTPClient:
    return CMSHTTPClientSingletonWrapper.get_instance()
