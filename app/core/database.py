from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import config


class AsyncDatabaseManager:

    def __init__(self) -> None:
        self._engine = create_async_engine(
            config.database.build_connection_str(), future=True, echo=True
        )

    async def close(self):
        await self._engine.dispose()

    def is_closed(self) -> bool:
        return self._engine is None

    def get_session(self):
        return async_sessionmaker(autocommit=False, autoflush=False, bind=self._engine)()


async_db_manager = AsyncDatabaseManager()


# async def commit_rollback():
#     try:
#         await db.commit()
#     except Exception:
#         await db.rollback()
#         raise
