from datetime import date

import pytest

from src.data_source import local


class TestGetCurrency:
    def test_get_currency(self, mocker):
        # GIVEN
        mocker.patch(
            "src.data_source.local.load_json_file",
            return_value={"EUR": [{"rate": 1.0, "date": "2023-09-28"}]},
        )

        # WHEN
        currency = local.LocalSource(None).get_currency("EUR")

        # THEN
        assert isinstance(currency, local.Currency)
        assert currency.name == "EUR"
        assert currency.rate == 1.0
        assert currency.date == date.fromisoformat("2023-09-28")

    def test_get_currency_exception(self, mocker):
        mocker.patch(
            "src.data_source.local.load_json_file",
            return_value={"EUR": [{"rate": 1.0, "date": "2023-09-28"}]},
        )

        msg = "Currency 'XXX' does not exist in the source file 'test.txt'"
        with pytest.raises(Exception, match=msg):
            local.LocalSource("test.txt").get_currency("XXX")
