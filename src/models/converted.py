from sqlalchemy import Column, Float, Integer, String

from src.connectors.database.session import Base


class ConvertedPricePLNSchema(Base):
    """Database schema for converted currency."""

    __tablename__ = "converted_price_pln"

    id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(String(3))
    rate = Column(Float(precision=4))
    price_in_pln = Column(Float(precision=2))
    date = Column(String)

    def to_dict(self) -> dict:
        """Method to dump SQLAlchemy object to a dictionary.

        Returns:
            dict: ConvertedPricePLNSchema object as a dictionary.
        """
        return {
            "id": self.id,
            "currency": self.currency,
            "rate": round(self.rate, 4),
            "price_in_pln": round(self.price_in_pln, 2),
            "date": self.date,
        }
