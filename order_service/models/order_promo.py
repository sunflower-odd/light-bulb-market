from sqlalchemy import Column, Integer,  ForeignKey
from order_service.db import Base

class OrderPromo(Base):
    __tablename__ = "order_promos"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    promo_id = Column(Integer, nullable=False)
    discount_percent = Column(Integer, nullable=False)