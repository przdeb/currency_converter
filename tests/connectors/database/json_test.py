import pytest

from src.connectors.database.json import JsonFileDatabaseConnector
from src.currency_converter import ConvertedPricePLN


class TestGetAll:
    def test_get_all(self, mocker):
        # GIVEN
        expected = {
            "1": {
                "id": 1,
                "currency": "eur",
                "rate": 4.6285,
                "price_in_pln": 21.1,
                "date": "2010-01-01",
            }
        }
        mocker.patch("src.connectors.database.json.load_json_file", return_value=expected)

        # WHEN
        result = JsonFileDatabaseConnector().get_all()

        # THEN
        assert result == list(expected.values())


class TestGetById:
    test_dict = {
        "id": 1,
        "currency": "eur",
        "rate": 4.6285,
        "price_in_pln": 21.1,
        "date": "2010-01-01",
    }
    test_data = [({"1": test_dict}, test_dict), ({}, {})]

    @pytest.mark.parametrize("data, expected", test_data)
    def test_get_by_id(self, data, expected, mocker):
        # GIVEN
        mocker.patch("src.connectors.database.json.load_json_file", return_value=data)

        # WHEN
        result = JsonFileDatabaseConnector().get_by_id(1)

        # THEN
        assert result == expected


class TestSave:
    def test_save(self, mocker):
        # GIVEN
        data = {
            "1": {
                "id": 1,
                "currency": "eur",
                "rate": 4.6285,
                "price_in_pln": 21.1,
                "date": "2010-01-01",
            }
        }
        mocker.patch("src.connectors.database.json.load_json_file", return_value=data)
        mocker.patch("src.connectors.database.json.save_json_file")
        test_entity = ConvertedPricePLN(1.23, "USD", 4.56, "2023-09-28", 7.89)

        # WHEN
        result = JsonFileDatabaseConnector().save(test_entity)

        # THEN
        assert result == int(list(data.keys())[0]) + 1

    def test_save_empty_database(self, mocker):
        # GIVEN
        data = {}
        mocker.patch("src.connectors.database.json.load_json_file", return_value=data)
        mocker.patch("src.connectors.database.json.save_json_file")
        test_entity = ConvertedPricePLN(1.23, "USD", 4.56, "2023-09-28", 7.89)

        # WHEN
        result = JsonFileDatabaseConnector().save(test_entity)

        # THEN
        assert result == 1
