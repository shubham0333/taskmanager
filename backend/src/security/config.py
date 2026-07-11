# 
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

print("DATABASE_URL =", os.getenv("DATABASE_URL"))

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()