from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, validator


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AI Career Discovery Assistant"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60 * 24  # 24 hours
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # CORS
    CORS_ORIGINS: List[str] = []
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Google Gemini API
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-pro"
    
    # AWS S3 / MinIO
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "career-assistant"
    S3_ENDPOINT_URL: Optional[str] = None  # For MinIO in development
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "docx", "doc"]
    
    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Session
    SESSION_LIFETIME_HOURS: int = 24
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()