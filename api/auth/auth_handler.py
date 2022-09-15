import time

import jwt
from api.settings import APP_SETTINGS
from fastapi import HTTPException, status


def decode_jwt(token: str) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_token = jwt.decode(token, APP_SETTINGS['CREDENTIALS']['JWT_SECRET'],
                                   algorithms=[APP_SETTINGS['CREDENTIALS']['JWT_ALGORITHM']])
    except jwt.InvalidTokenError:
        raise credentials_exception

    return decoded_token if decoded_token["expires"] >= time.time() else None
