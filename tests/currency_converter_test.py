from datetime import date

import pytest

from src.currency_converter import ConvertedPricePLN, PriceCurrencyConverterToPLN

test_data = [
    (10, "EUR", 1.23, date(2023, 9, 28)),
    (10, "EUR", 0, date(2023, 9, 28)),
]


@pytest.mark.parametrize("price, name, rate, _date", test_data)
class TestConvertToPLN:
    def test_convert_to_pln(self, price, name, rate, _date):
        # GIVEN
        test_class = type(
            "TestClass", (PriceCurrencyConverterToPLN,), {"name": name, "rate": rate, "date": _date}
        )

        # WHEN
        converted = test_class().convert_to_pln(price=price)

        # THEN
        assert isinstance(converted, ConvertedPricePLN)
        assert converted.price_in_source_currency == price
        assert converted.currency == name
        assert converted.currency_rate == rate
        assert converted.currency_rate_fetch_date == _date
        assert converted.price_in_pln == price * rate
