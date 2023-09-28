import logging

from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from src.connectors.database.base_connector import BaseConnector
from src.connectors.database.session import engine
from src.currency_converter import ConvertedPricePLN
from src.models.converted import ConvertedPricePLNSchema

LOG = logging.getLogger(__name__)


class SqliteDatabaseConnector(BaseConnector):
    """_summary_

    Args:
        BaseConnector (_type_): _description_
    """

    def get_all(self) -> list[dict]:
        """_summary_

        Returns:
            list[dict]: _description_
        """
        with Session(engine) as session:
            response = session.query(ConvertedPricePLNSchema).all()
            return [entry.to_dict() for entry in response] if response else []

    def get_by_id(self, record_id: int) -> dict:
        """_summary_

        Args:
            record_id (int): _description_

        Returns:
            dict: _description_
        """
        with Session(engine) as session:
            response = (
                session.query(ConvertedPricePLNSchema)
                .where(ConvertedPricePLNSchema.id == record_id)
                .first()
            )

            return response.to_dict() if response else {}

    def save(self, entity: ConvertedPricePLN) -> int:
        """_summary_

        Args:
            entity (ConvertedPricePLN): _description_

        Returns:
            int: _description_
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
