from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App settings
    app_name: str = "PDF Extraction Backend"
    debug: bool = False

    # Redis settings
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str | None = None

    # Celery settings
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    celery_task_track_started: bool = True
    celery_task_time_limit: int = 300  # 5 minutes
    celery_result_expires: int = 3600  # 1 hour

    # File upload settings
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: set[str] = {".pdf"}
    upload_dir: str = "temp_uploads"

    # OCR settings
    tesseract_cmd: str | None = None  # Path to tesseract executable (None = auto-detect)
    ocr_language: str = "eng"  # Default OCR language

    # API settings
    api_v1_prefix: str = "/api/v1"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
