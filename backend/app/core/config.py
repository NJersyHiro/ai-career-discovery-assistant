from typing import List, Optional, Union
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
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str], None]) -> List[str]:
        if v is None:
            return ["http://localhost:3000", "http://localhost:3001"]
        if isinstance(v, str):
            if not v:  # Handle empty string
                return ["http://localhost:3000", "http://localhost:3001"]
            if v.startswith("["):
                # Try to parse as JSON array
                try:
                    import json
                    return json.loads(v)
                except (json.JSONDecodeError, ValueError):
                    pass
            # Parse comma-separated string
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["http://localhost:3000", "http://localhost:3001"]
    
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
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "docx", "doc"]
    
    @validator("ALLOWED_EXTENSIONS", pre=True)
    def assemble_allowed_extensions(cls, v: Union[str, List[str], None]) -> List[str]:
        if v is None:
            return ["pdf", "docx", "doc"]
        if isinstance(v, str):
            if not v:
                return ["pdf", "docx", "doc"]
            # Parse comma-separated string
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["pdf", "docx", "doc"]
    
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