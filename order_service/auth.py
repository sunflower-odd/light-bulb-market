from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import HTTPBearer
from fastapi.security import OAuth2PasswordBearer
from fastapi import  Depends, HTTPException

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None



security = HTTPBearer()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     payload = decode_token(token)
#
#     if not payload:
#         raise HTTPException(status_code=401, detail="Invalid token")
#
#     return payload

from fastapi import Depends, HTTPException
from order_service.auth import decode_token
from fastapi.security import HTTPBearer

security = HTTPBearer()

def get_current_user(token=Depends(security)):
    payload = decode_token(token.credentials)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"user_id": payload.get("user_id")}