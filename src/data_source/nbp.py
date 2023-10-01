import logging

import requests

from src.config import NBP_BASE_URL, NBP_ENDPOINT
from src.currency import Currency
from src.data_source import Source

LOG = logging.getLogger(__name__)


class NbpSource(Source):
    """Class providing an interface to get the currency details using NBP API as a source."""

    def __init__(self, base_url: str = NBP_BASE_URL, endpoint: str = NBP_ENDPOINT) -> None:
        """Init method.

        Args:
            base_url (str, optional): NBP API base url. Defaults to NBP_BASE_URL.
            endpoint (str, optional): NBP API endpoint. Defaults to NBP_ENDPOINT.
        """
        self.__url = base_url
        self.__endpoint = endpoint

    def get_currency(self, currency: str) -> Currency:
        """Method to send a request to NBP API and get currency details.

        Args:
            currency (str): Currency code.

        Raises:
            Exception: When API response is invalid.
            HTTPError: When API does not have data for given currency.

        Returns:
            Currency: Currency details.
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
