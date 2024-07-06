from dataclasses import dataclass

from environs import Env
from sqlalchemy import URL

env = Env()
# Read .env into os.environ
env.read_env()


@dataclass(frozen=True)
class DatabaseConfig:
    """Database connection variables"""

    name: str = env.str("DATABASE")
    user: str = env.str("PGUSER")
    passwd: str = env.str("PGPASSWORD")
    host: str = env.str("PGHOST")

    driver: str = "asyncpg"
    database_system: str = "postgresql"

    def build_connection_str(self) -> str:
        """
        This function build a connection string
        """
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            database=self.name,
            password=self.passwd,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass(frozen=True)
class CMSHTTPClientConfig:
    """CMSHTTPClient Configuration"""

    base_url: str = "https://pro-api.coinmarketcap.com"
    cmc_api_key: str = env.str("CMC_API_KEY")


@dataclass(frozen=True)
class AuthenticationConfig:
    """Authentication Configuration"""

    SECRET_KEY = "d914f2e80d32efc3506c84b2dee1a0a706595c38ef17218e89209983e4135a7c"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


@dataclass
class Config:
    """All in one configuration class"""

    project_name: str = "FastAPI React App"

    cmc_http_client = CMSHTTPClientConfig()
    database = DatabaseConfig()
    authentication = AuthenticationConfig()

    vite_port: str = env.str("VITE_PORT")


config = Config()
