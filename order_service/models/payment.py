from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from product_service.db import Base

class Payment(Base):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer,  ForeignKey("orders.order_id"), nullable=False)

    payment_type = Column(String(50))
    payment_system = Column(String(50))
    transaction_id = Column(String(50))

    payment_amount_rub = Column(Integer)
    payment_datetime = Column(DateTime(timezone=True))
    status = Column(String(50))
