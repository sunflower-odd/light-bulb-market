from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from product_service.db import Base


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=True)
    description = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())