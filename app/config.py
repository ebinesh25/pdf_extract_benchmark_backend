from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App settings
    app_name: str = "PDF Extraction Backend"
    debug: bool = False

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
