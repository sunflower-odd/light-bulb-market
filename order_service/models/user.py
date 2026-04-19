from sqlalchemy import Column, Integer, String, DateTime
from order_service.db import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(30))
    login = Column(String(50), unique=True, nullable=False)
    role = Column(String(30))
    password = Column(String(255), nullable=False)

    created_at = Column(DateTime(timezone=True))