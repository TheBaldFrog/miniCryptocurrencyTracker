from pydantic import BaseModel


class USD(BaseModel):
    percent_change_24h: float
    price: float


class Cryptocurrency(BaseModel):
    cmc_rank: int
    id: int
    quote: dict[str, USD]
    total_supply: float

    class Config:
        allow_population_by_field_name = True
