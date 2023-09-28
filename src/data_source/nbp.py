import logging

import requests

from src.config import NBP_BASE_URL, NBP_ENDPOINT
from src.currency import Currency
from src.data_source import Source

LOG = logging.getLogger(__name__)


class NbpSource(Source):
    """_summary_

    Args:
        Source (_type_): _description_
    """

    def __init__(self, base_url: str = NBP_BASE_URL, endpoint: str = NBP_ENDPOINT) -> None:
        """_summary_

        Args:
            base_url (str, optional): _description_. Defaults to NBP_BASE_URL.
            endpoint (str, optional): _description_. Defaults to NBP_ENDPOINT.
        """
        self.__url = base_url
        self.__endpoint = endpoint

    def get_currency(self, currency: str) -> Currency:
        """_summary_

        Args:
            currency (str): _description_

        Raises:
            Exception: _description_

        Returns:
            Currency: _description_
        """
        url = f"{self.__url}/{self.__endpoint}/{currency}"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
        except requests.HTTPError as e:
            LOG.error(e)
            raise

        try:
            rates = response.json()["rates"][0]
        except Exception as e:
            msg = f"Failed to get rate for currency '{currency}'"
            LOG.error(msg)
            raise Exception(msg) from e

        return Currency(name=currency, rate=rates["mid"], date=rates["effectiveDate"])
