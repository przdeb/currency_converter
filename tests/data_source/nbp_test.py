from datetime import date

import pytest
from requests import HTTPError

from src.data_source import nbp


class TestGetCurrency:
    def test_get_currency(self, mocker):
        # GIVEN
        mocked_requests = mocker.patch("src.data_source.nbp.requests")
        mocked_response = mocker.Mock()
        mocked_response.json.return_value = {"rates": [{"mid": 1, "effectiveDate": "2023-09-28"}]}
        mocked_requests.get.return_value = mocked_response

        # WHEN
        currency = nbp.NbpSource().get_currency("EUR")

        # THEN
        assert isinstance(currency, nbp.Currency)
        assert currency.name == "EUR"
        assert currency.rate == 1.0
        assert currency.date == date.fromisoformat("2023-09-28")

    def test_get_currency_raises_exception(self, mocker):
        # GIVEN
        mocker.patch("src.data_source.nbp.requests.get", side_effect=HTTPError("BOOM"))

        with pytest.raises(HTTPError, match="BOOM"):
            nbp.NbpSource().get_currency("EUR")
