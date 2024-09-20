import secrets
from typing import Annotated
from fastapi import Depends, HTTPException, status
from jwt_auth import decode_access_token
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


basic_auth = HTTPBasic()


def basic_auth_guard(
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)]
) -> str:
    """
    Basic authentication guard.

    Verifies the provided username and password against the configured credentials.
    Returns the authenticated username if the credentials are valid.
    Raises an HTTPException with a 401 Unauthorized status code if the credentials are invalid.
    """
    username, password = b'test', b'test'

    try:
        current_username_bytes = credentials.username.encode("utf8")
        current_password_bytes = credentials.password.encode("utf8")
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    is_correct_username = secrets.compare_digest(current_username_bytes, username)
    is_correct_password = secrets.compare_digest(current_password_bytes, password)

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username




def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_access_token(token)
    if token_data is None:
        raise credentials_exception
    return token_data
