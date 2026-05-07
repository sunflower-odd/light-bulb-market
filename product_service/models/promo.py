from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from product_service.db import Base

class Promo(Base):
    __tablename__ = "promos"

    promo_id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    description = Column(String(500))

    discount_percent = Column(Integer, default=10)

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())