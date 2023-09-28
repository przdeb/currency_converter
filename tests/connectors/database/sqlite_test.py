import pytest
from sqlalchemy import create_engine

import src.connectors.database.sqlite
from src.connectors.database.sqlite import SqliteDatabaseConnector
from src.currency_converter import ConvertedPricePLN
from src.models.converted import Base, ConvertedPricePLNSchema


class TestGetAll:
    test_object = ConvertedPricePLNSchema(
        id=1, currency="EUR", rate=1.2345, price_in_pln=2.34, date="2023-09-28"
    )
    test_data = [([test_object], [test_object.to_dict()]), ([], [])]

    @pytest.mark.parametrize("data, expected", test_data)
    def test_get_all(self, mocker, data, expected):
        # GIVEN
        mocked_session = mocker.patch("src.connectors.database.sqlite.Session")
        mocked_session.return_value.__enter__.return_value.query.return_value.all.return_value = (
            data
        )

        # WHEN
        result: ConvertedPricePLNSchema = SqliteDatabaseConnector().get_all()

        # THEN
        assert result == expected


class TestGetById:
    test_object = ConvertedPricePLNSchema(
        id=1, currency="EUR", rate=1.2345, price_in_pln=2.34, date="2023-09-28"
    )
    test_data = [(test_object, test_object.to_dict()), (None, {})]

    @pytest.mark.parametrize("data, expected", test_data)
    def test_get_by_id(self, mocker, data, expected):
        # GIVEN
        mocked_session = mocker.patch("src.connectors.database.sqlite.Session")
        mocked_query = mocked_session.return_value.__enter__.return_value.query.return_value
        mocked_query.where.return_value.first.return_value = data

        # WHEN
        result: ConvertedPricePLNSchema = SqliteDatabaseConnector().get_by_id(1)

        # THEN
        assert result == expected


class TestSave:
    def test_save(self, mocker):
        # GIVEN
        test_engine = create_engine("sqlite:///:memory:")

        mocker.patch.object(src.connectors.database.sqlite, "engine", test_engine)
        Base.metadata.create_all(test_engine)
        test_object = ConvertedPricePLN(
            price_in_source_currency=1,
            currency="EUR",
            currency_rate=1.2345,
            price_in_pln=2.34,
            currency_rate_fetch_date="2023-09-28",
        )

        # WHEN
        result = SqliteDatabaseConnector().save(test_object)
        all_result = SqliteDatabaseConnector().get_all()

        # THEN
        assert result == 1
        assert all_result == [
            {"id": 1, "currency": "EUR", "rate": 1.2345, "price_in_pln": 2.34, "date": "2023-09-28"}
        ]
