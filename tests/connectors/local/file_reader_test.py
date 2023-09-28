import json
import os
from datetime import date

import pytest

from src.config import PROJECT_ROOT
from src.connectors.local.file_reader import load_json_file, save_json_file


class TestLoadJsonFile:
    def test_load_json_file(self):
        # GIVEN
        test_file_name = PROJECT_ROOT.joinpath("tests/test_data/test_json_happy.json")
        with open(test_file_name, encoding="utf-8") as fh:
            expected = json.load(fh)

        # WHEN
        result = load_json_file(test_file_name)

        # THEN
        assert result == expected

    @pytest.mark.parametrize(
        "file_name",
        [
            "tests/test_data/test_json_unhappy.json",
            "tests/test_data/test_json_unhappy2.txt",
            "tests/test_data/test_json_unhappy3.json",
        ],
    )
    def test_load_json_file_raises_json_exception(self, file_name):
        test_file_name = PROJECT_ROOT.joinpath(file_name)

        with pytest.raises(json.JSONDecodeError):
            load_json_file(test_file_name)

    def test_load_json_file_raises_no_file_exception(self):
        with pytest.raises(FileNotFoundError):
            load_json_file("not-existing-file.json")


class TestSaveJsonFile:
    @pytest.mark.parametrize("data", [{"key": "value"}, [{"key": "value"}]])
    def test_save_json_file(self, data):
        # GIVEN
        test_file_name = PROJECT_ROOT.joinpath("tests/test_data/test_json_output.json")

        # WHEN
        save_json_file(test_file_name, data)

        # THEN
        with open(test_file_name, encoding="utf-8") as fh:
            result = json.load(fh)
        assert result == data
        if os.path.exists(test_file_name):
            os.remove(test_file_name)

    @pytest.mark.parametrize("data", [1, date(1234, 5, 6), (1,)])
    def test_save_json_file_raises_exception(self, data):
        msg = f"Invalid data format, expected 'dict' or 'list', got {type(data)}"
        with pytest.raises(Exception, match=msg):
            save_json_file("", data)
