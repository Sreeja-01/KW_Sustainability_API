"""
Main FastAPI application.
"""

import logging
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

# Import database
from app.db.session import engine, Base
from app.db import base

# Import API routers
from app.api.v1 import routes_auth
from app.api.v1 import routes_documents
from app.api.v1 import routes_insights


# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="KW Sustainability Backend API",
    docs_url="/docs",
    redoc_url="/redoc",
)


# --------------------------------------------------
# CORS Middleware
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Include API Routers
# --------------------------------------------------

app.include_router(
    routes_auth.router,
    prefix=settings.API_V1_STR,
    tags=["auth"],
)

app.include_router(
    routes_documents.router,
    prefix=settings.API_V1_STR,
    tags=["documents"],
)

app.include_router(
    routes_insights.router,
    prefix=settings.API_V1_STR,
    tags=["insights"],
)


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "KW Sustainability API",
        "status": "running",
    }


# --------------------------------------------------
# Startup Event
# --------------------------------------------------

@app.on_event("startup")
def startup():
    """
    Create database tables on startup
    """

    Base.metadata.create_all(bind=engine)

    logger.info("Database tables initialized")


# --------------------------------------------------
# Local Run
# --------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )