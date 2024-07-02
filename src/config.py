from dataclasses import dataclass

from environs import Env

env = Env()
# Read .env into os.environ
env.read_env()


@dataclass(frozen=True)
class CMSHTTPClientConfig:
    """CMSHTTPClient Configuration"""

    base_url: str = "https://pro-api.coinmarketcap.com"
    cmc_api_key: str = env.str("CMC_API_KEY")


@dataclass
class Config:
    """All in one configuration class"""

    cmc_http_client = CMSHTTPClientConfig()

    vite_port: str = env.str("VITE_PORT")


config = Config()
