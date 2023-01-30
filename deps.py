import json
from typing import Union, Any
from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from immudb import ImmudbClient

from jose import jwt
from pydantic import ValidationError
from schemas.auth import TokenPayload, SystemUser
from settings import Settings, get_settings

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


async def get_immudb_client(settings: Settings = Depends(get_settings)) -> ImmudbClient:
    client = ImmudbClient(f"{settings.immudb_host}:{settings.immudb_port}")
    client.login(settings.immudb_user, settings.immudb_password)
    yield client


async def get_current_user(
    token: str = Depends(reuseable_oauth),
    settings: Settings = Depends(get_settings),
    database: ImmudbClient = Depends(get_immudb_client),
) -> SystemUser:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.algorithm]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: Union[dict[str, Any], None] = database.get(token_data.sub.encode("utf-8"))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    user_decode = json.loads(user.value.decode("utf-8"))
    return SystemUser(**user_decode)
