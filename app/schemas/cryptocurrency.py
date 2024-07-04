from pydantic import BaseModel, Field


class USD(BaseModel):
    percent_change_24h: float = Field(examples=["-3.70119543"])
    percent_change_30d: float = Field(examples=["-13.38036914"])
    price: float = Field(examples=["59648.79175222376"])


class Quote(BaseModel):
    USD: USD


class Cryptocurrency(BaseModel):
    cmc_rank: int = Field(examples=["1"])
    id: int = Field(examples=["1"])
    name: str = Field(examples=["Bitcoin"])
    quote: Quote
    total_supply: float = Field(examples=["19719378"])