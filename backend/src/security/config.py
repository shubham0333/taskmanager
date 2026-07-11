# 
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    frontend_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    class Config:
        # This resolves correctly whether the application is started from the
        # repository root or Render's backend root directory.
        env_file = Path(__file__).resolve().parents[3] / ".env"
        extra = "ignore"

settings = Settings()
