from typing import List, Optional, Union, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, ConfigDict
import json


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
    CORS_ORIGINS: Optional[Union[str, List[str]]] = None
    
    @field_validator("CORS_ORIGINS", mode='before')
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str], None]) -> Optional[List[str]]:
        if v is None or v == "":
            return None
        if isinstance(v, str):
            # Parse comma-separated string
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v
    
    # Google Gemini API
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-pro"
    
    # AWS S3 / MinIO
    AWS_ACCESS_KEY_ID: str = "minioadmin"
    AWS_SECRET_ACCESS_KEY: str = "minioadmin"
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "career-assistant"
    S3_ENDPOINT_URL: Optional[str] = "http://minio:9000"  # For MinIO in development
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: Optional[List[str]] = None
    
    @field_validator("ALLOWED_EXTENSIONS", mode='before')
    @classmethod
    def assemble_allowed_extensions(cls, v: Union[str, List[str], None]) -> Optional[List[str]]:
        if v is None or v == "":
            return None
        if isinstance(v, str):
            # Parse comma-separated string
            return [ext.strip() for ext in v.split(",") if ext.strip()]
        return v
    
    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Session
    SESSION_LIFETIME_HOURS: int = 24
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Email (optional, for future use)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        json_schema_extra={
            "json_decode_error": "ignore"
        }
    )


settings = Settings()