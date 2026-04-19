from pydantic import BaseModel
from datetime import datetime


class ReviewBase(BaseModel):
    user_id: int
    product_id: int
    title: str
    description: str
    created_at: datetime


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    user_id: int | None = None
    product_id: int | None = None
    title: str | None = None
    description: str | None = None
    created_at: datetime | None = None


class ReviewResponse(ReviewBase):
    review_id: int

    class Config:
        from_attributes = True