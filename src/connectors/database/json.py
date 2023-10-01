import logging

from src.config import JSON_DATABASE_NAME
from src.connectors.database.base_connector import BaseConnector
from src.connectors.local.file_reader import load_json_file, save_json_file
from src.currency_converter import ConvertedPricePLN

LOG = logging.getLogger(__name__)


class JsonFileDatabaseConnector(BaseConnector):
    """Class providing an interface to interact with JSON database."""

    def __init__(self) -> None:
        """Init method. Loads the JSON database contents."""
        self.__source_file = JSON_DATABASE_NAME
        try:
            self._data = load_json_file(JSON_DATABASE_NAME)
        except FileNotFoundError:
            LOG.info(f"{JSON_DATABASE_NAME} will be created in project root")
            self._data = {}

    def get_all(self) -> list[dict]:
        """Method to get all records from a converted_price_pln table.

        Returns:
            list[dict]: List of ConvertedPricePLNSchema objects in dictionary representation.
        """
        return list(self._data.values())

    def get_by_id(self, record_id: int) -> dict:
        """Method to get a record from a converted_price_pln table by id.

        Args:
            record_id (int): ID of a record to be retrieved.

        Returns:
            dict: ConvertedPricePLNSchema in a dictionary representation.

        """
        if str(record_id) not in self._data:
            LOG.error(f"Invalid ID, entry with ID '{record_id}' does not exist")
            return {}

        return self._data[str(record_id)]

    def save(self, entity: ConvertedPricePLN) -> int:
        """Method to save ConvertedPricePLN in a database.

        Args:
            entity (ConvertedPricePLN): Record to be saved.

        Returns:
            int: ID of a newly added record.
        """
        new_entry_id = self.__get_max_id() + 1
        self._data[str(new_entry_id)] = entity.to_model(new_entry_id).model_dump()
        save_json_file(self.__source_file, self._data)
        return new_entry_id

    def __get_max_id(self) -> int:
        """Method to get the ID of the latest record in a database

        Returns:
            int: ID of a latest record.
        """
        try:
            return int(max(self._data.keys(), key=int))
        # In case of empty database, start with 0
        except ValueError:
            return 0
