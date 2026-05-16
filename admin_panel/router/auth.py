from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from order_service.db import get_db
from order_service.models.user import User
from ..core.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(email: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_access_token({
        "user_id": user.user_id,
        "email": user.email
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }