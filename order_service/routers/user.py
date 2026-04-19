from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from order_service.db import get_db
from order_service.models.user import User
from order_service.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_obj = User(**user.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(User).filter(User.user_id == user_id).first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")

    return db_obj


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_obj = db.query(User).filter(User.user_id == user_id).first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)

    db.commit()
    db.refresh(db_obj)

    return db_obj


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(User).filter(User.user_id == user_id).first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_obj)
    db.commit()

    return {"message": "User deleted successfully"}