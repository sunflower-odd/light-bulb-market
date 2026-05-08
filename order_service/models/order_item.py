from sqlalchemy import Column, Integer,  ForeignKey
from order_service.db import Base
from sqlalchemy import Numeric

class OrderItem(Base):
    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer)
    price = Column(Numeric, nullable=False)