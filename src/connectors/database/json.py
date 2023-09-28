import logging

from src.config import JSON_DATABASE_NAME
from src.connectors.database.base_connector import BaseConnector
from src.connectors.local.file_reader import load_json_file, save_json_file
from src.currency_converter import ConvertedPricePLN

LOG = logging.getLogger(__name__)


class JsonFileDatabaseConnector(BaseConnector):
    """_summary_

    Args:
        BaseConnector (_type_): _description_
    """

    def __init__(self) -> None:
        """_summary_"""
        self.__source_file = JSON_DATABASE_NAME
        try:
            self._data = load_json_file(JSON_DATABASE_NAME)
        except FileNotFoundError:
            LOG.info(f"{JSON_DATABASE_NAME} will be created in project root")
            self._data = {}

    def get_all(self) -> list[dict]:
        """_summary_

        Returns:
            list[dict]: _description_
        """
        return list(self._data.values())

    def get_by_id(self, record_id: int) -> dict:
        """_summary_

        Args:
            record_id (int): _description_

        Raises:
            Exception: _description_

        Returns:
            dict: _description_
        """
        if str(record_id) not in self._data:
            LOG.error(f"Invalid ID, entry with ID '{record_id}' does not exist")
            return {}

        return self._data[str(record_id)]

    def save(self, entity: ConvertedPricePLN) -> int:
        """_summary_

        Args:
            entity (ConvertedPricePLN): _description_

        Returns:
            int: _description_
        """
        new_entry_id = self.__get_max_id() + 1
        self._data[str(new_entry_id)] = entity.to_model(new_entry_id).model_dump()
        save_json_file(self.__source_file, self._data)
        return new_entry_id

    def __get_max_id(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        try:
            return int(max(self._data.keys(), key=int))
        # In case of empty database, start with 0
        except ValueError:
            return 0
