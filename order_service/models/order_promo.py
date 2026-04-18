from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from product_service.db import Base

class OrderPromo(Base):
    __tablename__ = "order_promos"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    promo_id = Column(Integer, ForeignKey("promos.promo_id"), nullable=False)