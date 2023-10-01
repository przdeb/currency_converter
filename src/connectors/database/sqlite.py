import logging

from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from src.connectors.database.base_connector import BaseConnector
from src.connectors.database.session import engine
from src.currency_converter import ConvertedPricePLN
from src.models.converted import ConvertedPricePLNSchema

LOG = logging.getLogger(__name__)


class SqliteDatabaseConnector(BaseConnector):
    """Class providing an interface to interact with SQLite database."""

    def get_all(self) -> list[dict]:
        """Method to get all records from a converted_price_pln table.

        Returns:
            list[dict]: List of ConvertedPricePLNSchema objects in dictionary representation.
        """
        with Session(engine) as session:
            response = session.query(ConvertedPricePLNSchema).all()
            return [entry.to_dict() for entry in response] if response else []

    def get_by_id(self, record_id: int) -> dict:
        """Method to get a record from a converted_price_pln table by id.

        Args:
            record_id (int): ID of a record to be retrieved.

        Returns:
            dict: ConvertedPricePLNSchema in a dictionary representation.
        """
        with Session(engine) as session:
            response = (
                session.query(ConvertedPricePLNSchema)
                .where(ConvertedPricePLNSchema.id == record_id)
                .first()
            )

            return response.to_dict() if response else {}

    def save(self, entity: ConvertedPricePLN) -> int:
        """Method to save ConvertedPricePLN in a database.

        Args:
            entity (ConvertedPricePLN): Record to be saved.

        Returns:
            int: ID of a newly added record.
        """

        with Session(engine) as session, session.begin():
            entry = ConvertedPricePLNSchema(
                currency=entity.currency,
                rate=entity.currency_rate,
                price_in_pln=entity.price_in_pln,
                date=entity.currency_rate_fetch_date,
            )
            session.add(entry)
            try:
                session.flush()
            except OperationalError as e:
                LOG.error(f"Failed to save data: {e}")
                raise
            return entry.id
