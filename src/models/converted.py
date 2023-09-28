from sqlalchemy import Column, Float, Integer, String

from src.connectors.database.session import Base


class ConvertedPricePLNSchema(Base):
    """_summary_"""

    __tablename__ = "converted_price_pln"

    id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(String(3))
    rate = Column(Float(precision=4))
    price_in_pln = Column(Float(precision=2))
    date = Column(String)

    def to_dict(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return {
            "id": self.id,
            "currency": self.currency,
            "rate": round(self.rate, 4),
            "price_in_pln": round(self.price_in_pln, 2),
            "date": self.date,
        }
