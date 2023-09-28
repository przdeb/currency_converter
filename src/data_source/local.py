import logging

from src.connectors.local.file_reader import load_json_file
from src.currency import Currency
from src.data_source import Source

LOG = logging.getLogger(__name__)


class LocalSource(Source):
    """_summary_"""

    def __init__(self, local_source_file_name: str = "example_currency_rates.json") -> None:
        """_summary_

        Args:
            local_source_file_name (str, optional): _description_.
                Defaults to "example_currency_rates.json".
        """
        self.__source_file = local_source_file_name
        self._data = load_json_file(local_source_file_name)

    def get_currency(self, currency: str) -> Currency:
        """_summary_

        Args:
            currency (str): _description_

        Raises:
            Exception: _description_

        Returns:
            Currency: _description_
        """
        if currency.upper() not in (_currency.upper() for _currency in self._data.keys()):
            msg = (
                f"Currency '{currency.upper()}' does not exist in the "
                f"source file '{self.__source_file}'"
            )
            LOG.error(msg)
            raise Exception(msg)

        return Currency(name=currency, **self._data[currency.upper()][0])
