from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Set


class Settings(BaseSettings):
    # App settings
    app_name: str = "PDF Extraction Backend"
    debug: bool = False
    env: str = "dev"  # dev | prod

    # File upload settings
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: Set[str] = {".pdf"}
    upload_dir: str = "temp_uploads"

    # OCR settings
    tesseract_cmd: str | None = None
    ocr_language: str = "eng"

    # API settings
    api_v1_prefix: str = "/api/v1"

    # MongoDB
    mongo_uri: str = "mongodb://localhost:27017"

    @property
    def mongo_db_name(self) -> str:
        """
        Automatically choose DB based on environment
        """
        return (
            "production_pdf_tools"
            if self.env.lower() == "prod"
            else "dev_pdf_tools"
        )

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
