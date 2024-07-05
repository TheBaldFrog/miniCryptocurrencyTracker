from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.dependencies import get_cmc_client, get_db
from app.dto.model.user import User
from app.dto.schema.cryptocurrency import CryptocurrencySchema
from app.service.coinmarketcap.cmc_http_client import CMSHTTPClient

cryptocurrencies = APIRouter(prefix="/cryptocurrencies", tags=["Cryptocurrencies"])


@cryptocurrencies.get("/")
async def get_cryptocurrencies(
    cmc_client: Annotated[CMSHTTPClient, Depends(get_cmc_client)]
) -> list[CryptocurrencySchema]:
    return await cmc_client.get_listings()


@cryptocurrencies.get("/{currency_id}")
async def get_cryptocurrency(
    currency_id: int, cmc_client: Annotated[CMSHTTPClient, Depends(get_cmc_client)]
) -> CryptocurrencySchema:
    return await cmc_client.get_currencies(currency_id)


@cryptocurrencies.get("/testdb/")
async def get_testdb(db: AsyncSession = Depends(get_db)):
    db_user = User(
        username="fs7",
        email="qw7",
        first_name="fdsf",
        last_name="sdfsdf",
        hashed_password="fsdfsddsfsdfsdfd",
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # db_user.username = "fsdfsdc1111111111111111111111"
    # await db.commit()

    # some_squidward = await db.get(User, 4)
    # print(some_squidward.id)
    #
    # result = await db.execute(select(User).where(User.id == 1))
    # user = result.scalar_one()
    # print(user.id)
    # print(user.email)
    # user.email = "FFF"
    # await db.commit()

    # result = await db.execute(select(User).where(User.id == 4))
    # user = result.scalar_one_or_none()
    # if user is not None:
    #     await db.delete(user)
    #     await db.commit()

    # result = await db.get(User, 4)
    # await db.delete(result)
    # await db.commit()

    return {"dsfsd": "fdsfsd"}
