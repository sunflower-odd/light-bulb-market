from sqlalchemy import Column, Integer, String, ForeignKey
from order_service.db import Base

class Address(Base):
    __tablename__ = "addresses"

    address_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    city = Column(String(50))
    street = Column(String(50))
    house = Column(Integer)
    apartment = Column(Integer)
    postal_code = Column(Integer)
