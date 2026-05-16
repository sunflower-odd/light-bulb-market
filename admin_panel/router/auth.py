from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import requests

from core.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    email: str


@router.post("/login")
def login(data: LoginRequest):
    print(f'auth_router ########################################## {data.email}')
    response = requests.get(
        "http://order_app:8000/users/by-email",
        params={"email": data.email},
        timeout=5
    )

    if response.status_code != 200:
        print("ORDER APP ERROR:", response.status_code, response.text)
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )
    user = response.json()

    token = create_access_token({
        "user_id": user["user_id"],
        "email": user["email"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }