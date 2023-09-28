from argparse import Namespace
from datetime import date

import pytest

from src.currency import Currency
from src.currency_converter import ConvertedPricePLN
from src.main import get_currency, main


class TestGetCurrency:
    def test_get_currency_local_source(self, mocker):
        # GIVEN
        args = Namespace(source="LOCAL", file="test.txt", currency="EUR")
        # Mock class
        mock = mocker.patch("src.main.LocalSource")
        # Mock instance
        mocked_local_source = mock.return_value
        # Mock instance method
        mocked_get_currency = mocked_local_source.get_currency
        mocked_get_currency.return_value = "Currency"

        # WHEN
        result = get_currency(args)

        # THEN
        assert result == "Currency"
        mock.assert_called_once_with("test.txt")
        mocked_get_currency.assert_called_once_with("EUR")

    def test_get_currency_nbp_source(self, mocker):
        # GIVEN
        args = Namespace(source="NBP", currency="EUR")
        # Mock class
        mock = mocker.patch("src.main.NbpSource")
        # Mock instance
        mocked_nbp_source = mock.return_value
        # Mock method
        mocked_nbp_source.get_currency.return_value = "Currency"

        # WHEN
        result = get_currency(args)

        # THEN
        assert result == "Currency"
        mock.assert_called_once_with()
        mocked_nbp_source.get_currency.assert_called_once_with("EUR")

    def test_get_currency_invalid_source(self):
        args = Namespace(source="NotSupported", currency="EUR")

        with pytest.raises(Exception, match="Source not available... yet"):
            get_currency(args)


class TestMain:
    test_data = [
        (
            Namespace(
                amount=1, currency="EUR", source="LOCAL", file="test.json", env="dev", debug="False"
            ),
            Currency(name="EUR", rate=1, date="2023-09-28"),
            ConvertedPricePLN(
                price_in_source_currency=1,
                currency="EUR",
                currency_rate=1.0,
                currency_rate_fetch_date=date(2023, 9, 28),
                price_in_pln=1.0,
            ),
        ),
        (
            Namespace(amount=1, currency="USD", source="NBP", env="prod", debug="True"),
            Currency(name="USD", rate=18, date="2022-02-22"),
            ConvertedPricePLN(
                price_in_source_currency=1,
                currency="USD",
                currency_rate=18.0,
                currency_rate_fetch_date=date(2022, 2, 22),
                price_in_pln=18.0,
            ),
        ),
    ]

    @pytest.mark.parametrize("namespace, currency, expected", test_data)
    def test_main(self, mocker, namespace, currency, expected):
        # GIVEN
        mocked_parse_arguments = mocker.patch("src.main.parse_arguments", return_value=namespace)
        mocked_get_currency = mocker.patch("src.main.get_currency", return_value=currency)
        mocked_db_connector = mocker.patch("src.main.DatabaseConnector")

        # WHEN
        result = main()

        # THEN
        mocked_parse_arguments.assert_called_once()
        mocked_get_currency.assert_called_once_with(namespace)
        mocked_db_connector.assert_called_once_with(namespace.env)
        assert isinstance(result, ConvertedPricePLN)
        assert result == expected
