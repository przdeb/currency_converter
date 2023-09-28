from abc import ABC, abstractmethod

from src.currency_converter import ConvertedPricePLN


class BaseConnector(ABC):
    @abstractmethod
    def save(self, entity: ConvertedPricePLN) -> int:
        ...

    @abstractmethod
    def get_all(self) -> list[dict]:
        ...

    @abstractmethod
    def get_by_id(self, record_id: int) -> dict:
        ...
