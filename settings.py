from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    immudb_host: str
    immudb_port: int
    immudb_user: str
    immudb_password: str
    jwt_secret_key: str
    jwt_refresh_secret_key: str

    app_name: str = "CodeNotary API"
    access_token_expire_minutes: int = 30  # 30 minutes
    refresh_token_expire_minutes: int = 60 * 24 * 7 # 7 days
    algorithm: str = "HS256"
    chunk_size: int = 100

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
