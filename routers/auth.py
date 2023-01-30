import json
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from immudb import ImmudbClient

from schemas.auth import TokenSchema, UserAuth, UserOut, SystemUser

from auth import (
    verify_password,
    create_access_token,
    get_hashed_password,
    create_refresh_token,
)
from deps import get_current_user, get_immudb_client

router = APIRouter()


@router.post("/signup", summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth, database: ImmudbClient = Depends(get_immudb_client)):
    user = database.get(data.email.encode("utf-8"))
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist",
        )
    user = {
        "email": data.email,
        "password": get_hashed_password(data.password),
        "id": str(uuid4()),
    }
    user_json = json.dumps(user, indent=2).encode("utf-8")
    database.set(data.email.encode("utf-8"), user_json)
    return user


@router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    database: ImmudbClient = Depends(get_immudb_client),
):
    result = database.get(form_data.username.encode("utf-8"))
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    user_decode = json.loads(result.value.decode("utf-8"))
    hashed_pass = user_decode["password"]
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    return {
        "access_token": create_access_token(user_decode["email"]),
        "refresh_token": create_refresh_token(user_decode["email"]),
    }


@router.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: SystemUser = Depends(get_current_user)):
    return user