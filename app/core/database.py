from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import config
from app.dto.model import Base


class AsyncDatabaseManager:

    def __init__(self) -> None:
        self._engine = create_async_engine(
            config.database.build_connection_str(), future=True, echo=True
        )
        self._async_session: AsyncSession | None = None

    async def close(self):
        await self._engine.dispose()

    async def init(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    def is_closed(self) -> bool:
        return self._engine is None

    def get_new_session(self) -> AsyncSession:
        self._async_session = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )()
        return self._async_session

    def get_session(self) -> AsyncSession:
        if self._async_session is None:
            self.get_new_session()
        return self._async_session


async_db_manager = AsyncDatabaseManager()
