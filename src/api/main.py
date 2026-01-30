"""FastAPI application entry point for DiagnoML."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import __version__

app = FastAPI(
    title="DiagnoML API",
    description="Clinical Diagnosis Prediction API",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        Health status response.
    """
    return {"status": "healthy", "version": __version__}


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint.

    Returns:
        Welcome message.
    """
    return {"message": "Welcome to DiagnoML API", "version": __version__}
