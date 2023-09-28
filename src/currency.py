from datetime import date
from typing import Annotated

from pydantic import BaseModel, StringConstraints

from src.currency_converter import PriceCurrencyConverterToPLN


class Currency(BaseModel, PriceCurrencyConverterToPLN):
    name: Annotated[str, StringConstraints(to_upper=True, pattern=r"^[a-zA-Z]{3}$")]
    rate: float
    date: date
