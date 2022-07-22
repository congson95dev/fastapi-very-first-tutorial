from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel


# This solution using HTTPBearer to authenticate
# So we don't need to use username and password to authenticate
# Just need to transfer the token


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


app = FastAPI()


def create_access_token(expires_delta: Union[timedelta, None] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode = {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def check_access_token(credentials: HTTPBasicCredentials = Depends(HTTPBearer())):
    """
        Function that is used to validate the token in the case that it requires it
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials

    try:
        payload = jwt.decode(token, key='secret', options={"verify_signature": False,
                                                           "verify_aud": False,
                                                           "verify_iss": False})
        if payload is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception


@app.post("/token", response_model=Token)
async def action_create_access_token():
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/test", dependencies=[Depends(check_access_token)])
async def test():
    return {"Granted": True}
