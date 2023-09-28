from dataclasses import dataclass
from datetime import date
from typing import Annotated

from pydantic import BaseModel, StringConstraints, field_validator


@dataclass(frozen=True)
class ConvertedPricePLN:
    price_in_source_currency: float
    currency: str
    currency_rate: float
    currency_rate_fetch_date: str
    price_in_pln: float

    def to_model(self, record_id: int):
        """_summary_

        Args:
            record_id (int): _description_

        Returns:
            _type_: _description_
        """
        return ConvertedPricePLNModel(
            id=record_id,
            currency=self.currency,
            rate=self.currency_rate,
            price_in_pln=self.price_in_pln,
            date=self.currency_rate_fetch_date,
        )


class ConvertedPricePLNModel(BaseModel):
    id: int
    currency: Annotated[str, StringConstraints(to_upper=True, pattern=r"^[a-zA-Z]{3}$")]
    rate: float
    price_in_pln: float
    date: date

    @field_validator("price_in_pln", mode="before")
    def trim_price(cls, value):
        if isinstance(value, float):
            return round(value, 2)
        return value

    @field_validator("rate", mode="before")
    def trim_rate(cls, value):
        if isinstance(value, float):
            return round(value, 4)
        return value


class PriceCurrencyConverterToPLN:
    def convert_to_pln(self, *, price: float) -> ConvertedPricePLN:
        """_summary_

        Args:
            price (float): _description_

        Returns:
            ConvertedPricePLN: _description_
        """
        return ConvertedPricePLN(
            price_in_source_currency=price,
            currency=self.name,
            currency_rate=self.rate,
            currency_rate_fetch_date=self.date,
            price_in_pln=price * self.rate,
        )
