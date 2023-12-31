from abc import ABC, abstractmethod


class Source(ABC):
    @abstractmethod
    def get_currency(self, currency: str):
        ...
