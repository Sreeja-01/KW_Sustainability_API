"""
Main FastAPI application
"""

import logging
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

# Database
from app.db.session import engine, Base
from app.db import base

# Routes
from app.api.v1 import routes_auth
from app.api.v1 import routes_documents
from app.api.v1 import routes_insights
from app.api.v1 import routes_search


# ---------------------------------------------------
# Logging
# ---------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------------------------------
# FastAPI App
# ---------------------------------------------------

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="KW Sustainability Backend API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ---------------------------------------------------
# CORS
# ---------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------
# API ROUTERS
# ---------------------------------------------------

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

app.include_router(
    routes_search.router,
    prefix=settings.API_V1_STR,
    tags=["search"],
)


# ---------------------------------------------------
# ROOT
# ---------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "KW Sustainability API",
        "status": "running"
    }


# ---------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ---------------------------------------------------
# STARTUP EVENT
# ---------------------------------------------------

@app.on_event("startup")
def startup():

    Base.metadata.create_all(bind=engine)

    logger.info("Database tables initialized")


# ---------------------------------------------------
# LOCAL RUN
# ---------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )