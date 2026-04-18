from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from product_service.db import Base

class Delivery(Base):
    __tablename__ = "deliveries"
    __table_args__ = {"extend_existing": True}

    delivery_id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    address_id = Column(Integer, ForeignKey("addresses.address_id"), nullable=False)

    courier_service = Column(String(255), nullable=False)
    tracking_number = Column(String(100), unique=True)

    delivery_date = Column(DateTime(timezone=True))
    delivery_status = Column(String(50), default="pending")
