from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    model = None

    @classmethod
    async def create(cls, db: AsyncSession, orm_model: model):
        db.add(orm_model)

        try:
            await db.commit()
            await db.refresh(orm_model)
        except Exception:
            await db.rollback()
            raise

        return orm_model

    @classmethod
    async def get_all(cls, db: AsyncSession, skip: int = 0, limit: int = 100):
        query = select(cls.model).order_by(cls.model.id).offset(skip).limit(limit)
        result = await db.execute(query)
        return (await db.execute(query)).scalars().all()

    @classmethod
    async def get_by_id(cls, db: AsyncSession, model_id: int) -> model:
        query = select(cls.model).where(cls.model.id == model_id)
        result = (await db.execute(query)).scalar_one_or_none()

        return result

    @classmethod
    async def update(cls, db: AsyncSession, orm_model: model):

        m = orm_model
        try:
            await db.commit()
            await db.refresh(m)
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def delete(cls, db: AsyncSession, orm_model: model):
        await db.delete(orm_model)

        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def delete_by_id(cls, db: AsyncSession, model_id: int):
        query = delete(cls.model).where(cls.model.id == model_id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
