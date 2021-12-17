from pydantic import BaseSettings


class Settings(BaseSettings):
    BYBIT_API_KEY: str
    BYBIT_SECRET_KEY: str
    API_BASE_URL: str
    API_NAME: str

    class Config:
        env_file = "../.env"
