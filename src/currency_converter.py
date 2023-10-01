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

    def to_model(self, record_id: int) -> "ConvertedPricePLNModel":
        """Method converts dataclass object to Pydantic model.

        Args:
            record_id (int): ID of a converted currency; used as an ID in JSON database.

        Returns:
            ConvertedPricePLNModel: Converted currency model.
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
        """Method that converts currency to PLN.

        Args:
            price (float): Amount of money to be converted.

        Returns:
            ConvertedPricePLN: Currency converted to PLN.
        """
        return ConvertedPricePLN(
            price_in_source_currency=price,
            currency=self.name,
            currency_rate=self.rate,
            currency_rate_fetch_date=self.date,
            price_in_pln=price * self.rate,
        )
