from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routes import extraction, benchmarking

from app.dependencies import connect_to_mongo, close_mongo

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    description="PDF extraction backend with multiple extraction tools",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(extraction.router, prefix=settings.api_v1_prefix)
app.include_router(benchmarking.router, prefix=settings.api_v1_prefix)

MODELS_LIST = [
    {
        "name": "pymupdf",
        "description": "PyMuPDF (fitz) is a PDF library based on the MuPDF open source project.",
        "tags": ["opensource"],
    },
    {
        "name": "pdfplumber",
        "description": "pdfplumber is a PDF library based on the MuPDF open source project.",
        "tags": ["OCR", "opensource"],
    },
    {
        "name": "pypdf",
        "description": "pypdf is a PDF library based on the MuPDF open source project.",
        "tags": ["opensource", "tables"],
    },
    {
        "name": "pdfminer",
        "description": "pdfminer is a PDF library based on the MuPDF open source project.",
        "tags": ["opensource"],
    },
]

@app.on_event("startup")
async def startup():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown():
    await close_mongo()

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "description": "PDF extraction backend supporting multiple extraction tools",
        "docs": "/docs",
        "available_tools": MODELS_LIST
    }

@app.get("/models")
async def get_models():
    """Get available models."""
    return MODELS_LIST

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/health/db")
async def db_health_check():
    """Health check endpoint for Database."""
    collections = await db.list_collection_names()
    return {
        "db": db.name,
        "collections": collections
    }
