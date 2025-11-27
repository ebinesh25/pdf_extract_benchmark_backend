import os
import uuid
import aiofiles
from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.config import get_settings

settings = get_settings()


async def validate_pdf_file(file: UploadFile) -> None:
    """
    Validate uploaded PDF file.

    Args:
        file: The uploaded file

    Raises:
        HTTPException: If validation fails
    """
    # Check file extension
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(settings.allowed_extensions)}"
        )

    # Check content type
    if file.content_type not in ["application/pdf", "application/x-pdf"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid content type. Must be application/pdf"
        )


async def save_upload_file(file: UploadFile) -> str:
    """
    Save uploaded file to temporary directory.

    Args:
        file: The uploaded file

    Returns:
        str: Path to the saved file
    """
    # Create upload directory if it doesn't exist
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Generate unique filename
    file_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix
    file_path = upload_dir / f"{file_id}{file_extension}"

    # Save file
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()

        # Check file size
        if len(content) > settings.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.max_file_size / (1024 * 1024):.1f}MB"
            )

        await f.write(content)

    return str(file_path)


def delete_file(file_path: str) -> None:
    """
    Delete a file from the filesystem.

    Args:
        file_path: Path to the file to delete
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        # Log error but don't raise - cleanup failures shouldn't break the app
        print(f"Error deleting file {file_path}: {e}")


def cleanup_old_files(max_age_hours: int = 24) -> None:
    """
    Clean up old files from the upload directory.

    Args:
        max_age_hours: Maximum age of files in hours before deletion
    """
    upload_dir = Path(settings.upload_dir)
    if not upload_dir.exists():
        return

    import time
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600

    for file_path in upload_dir.iterdir():
        if file_path.is_file():
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_seconds:
                delete_file(str(file_path))
