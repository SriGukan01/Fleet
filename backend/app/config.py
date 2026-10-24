import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "VERITRUST AI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # Security
    JWT_SECRET_KEY: str = "veritrust-super-secret-key-sih-2026-production-ready"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours for hackathon evaluation
    
    # Database
    MONGODB_URL: Optional[str] = None  # e.g. "mongodb+srv://user:pass@cluster.mongodb.net/veritrust"
    MONGODB_DB_NAME: str = "veritrust_ai"
    
    # Storage
    STORAGE_TYPE: str = "local"  # "local" or "s3"
    STORAGE_LOCAL_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage")
    
    # AI & Verification Providers
    AI_PROVIDER: str = "local"  # "local", "mock", "openai", "gemini"
    AI_API_KEY: Optional[str] = None
    DIGILOCKER_SANDBOX_MODE: bool = True
    
    # Limits
    MAX_FILE_SIZE_MB: int = 25
    MAX_PAGE_COUNT: int = 30
    ALLOWED_MIME_TYPES: list[str] = [
        "application/pdf",
        "image/png",
        "image/jpeg",
        "image/webp"
    ]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

# Ensure storage directories exist
os.makedirs(settings.STORAGE_LOCAL_DIR, exist_ok=True)
os.makedirs(os.path.join(settings.STORAGE_LOCAL_DIR, "uploads"), exist_ok=True)
os.makedirs(os.path.join(settings.STORAGE_LOCAL_DIR, "previews"), exist_ok=True)
os.makedirs(os.path.join(settings.STORAGE_LOCAL_DIR, "reports"), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"), exist_ok=True)
