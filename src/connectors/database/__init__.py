from typing import Literal

from src.connectors.database.json import JsonFileDatabaseConnector
from src.connectors.database.sqlite import SqliteDatabaseConnector


class DatabaseConnector:
    def __init__(self, environment: Literal["PROD", "DEV"]) -> None:
        if environment == "PROD":
            self.connector = SqliteDatabaseConnector()
        else:
            self.connector = JsonFileDatabaseConnector()
