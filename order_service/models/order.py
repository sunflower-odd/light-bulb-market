from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from order_service.db import Base

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    amount_rub = Column(Integer)
    status = Column(String(50))

    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
