from fastapi import APIRouter, Depends, HTTPException, Header
from typing import List
from sqlalchemy.orm import Session

from order_service.db import get_db
from order_service.models.user import User
from order_service.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])
router_auth = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/me", response_model=UserResponse)
def get_me(
    x_user_id: int = Header(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.user_id == x_user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user

@router.get("/by-email")
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    print("HIT BY EMAIL", email)
    print(f'USER ##################### {email}')
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404)

    return {
        "user_id": user.user_id,
        "email": user.email
    }

# @router.get("/{user_id}", response_model=UserResponse)
# def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
#     db_obj = db.query(User).filter(User.user_id == user_id).first()
#
#     if not db_obj:
#         raise HTTPException(status_code=404, detail="User not found")
#
#     return db_obj


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_obj = User(**user.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
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

