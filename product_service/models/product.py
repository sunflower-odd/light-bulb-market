from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from product_service.db import Base

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    image_url = Column(String(255))
    price = Column(Float)
    description = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
