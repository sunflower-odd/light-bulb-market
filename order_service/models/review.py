from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from order_service.db import Base

class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    product_id = Column(Integer, nullable=False)

    title = Column(String(50))
    description = Column(String(500))
    created_at = Column(DateTime(timezone=True))
