from fastapi import Depends, HTTPException, status
from typing_extensions import Annotated
from mock_up_data import fake_users
from jose import jwt, JWTError
from consts import SECRET_KEY, ALGORITHM
from login import oauth2_scheme
from utils import get_user


async def protected_route(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users, username)
    if user is None:
        raise credentials_exception
    return user
