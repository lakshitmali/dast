"""
DAST Platform — FastAPI Application Entry Point
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import init_db

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown hooks."""
    logger.info("=" * 60)
    logger.info("  DAST Platform — Starting Up")
    logger.info("=" * 60)

    # Initialize database tables (dev mode)
    try:
        await init_db()
        logger.info("✓ Database tables initialized")
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")

    # Verify Redis connectivity
    try:
        import redis.asyncio as aioredis
        r = aioredis.from_url(settings.REDIS_URL)
        await r.ping()
        await r.close()
        logger.info("✓ Redis connection verified")
    except Exception as e:
        logger.warning(f"✗ Redis connection failed: {e}")

    logger.info(f"  Backend URL: {settings.BACKEND_URL}")
    logger.info(f"  Frontend URL: {settings.FRONTEND_URL}")
    logger.info("=" * 60)

    yield

    logger.info("DAST Platform — Shutting Down")


# ─── Create FastAPI Application ──────────────────────────────────────────────
app = FastAPI(
    title="DAST Platform API",
    description="Dynamic Application Security Testing Platform — REST API & WebSocket Server",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)


@app.exception_handler(ConnectionRefusedError)
async def database_connection_error(request: Request, exc: ConnectionRefusedError):
    """Turn unavailable local services into an actionable, non-secret error."""
    logger.exception("database_connection_failed path=%s", request.url.path)
    return JSONResponse(
        status_code=503,
        content={
            "error": "Database unavailable",
            "detail": "PostgreSQL is not reachable. Start PostgreSQL and verify DATABASE_URL.",
            "component": "database",
        },
    )


@app.exception_handler(SQLAlchemyError)
async def database_query_error(request: Request, exc: SQLAlchemyError):
    logger.exception("database_query_failed path=%s", request.url.path)
    return JSONResponse(
        status_code=503,
        content={
            "error": "Database unavailable",
            "detail": "The database operation could not be completed. Verify PostgreSQL and migrations.",
            "component": "database",
        },
    )

# ─── CORS Middleware ─────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Register Routers ───────────────────────────────────────────────────────
from app.api.auth import router as auth_router
from app.api.scans import router as scans_router
from app.api.reports import router as reports_router
from app.api.websocket import router as ws_router

app.include_router(auth_router)
app.include_router(scans_router)
app.include_router(reports_router)
app.include_router(ws_router)


# ─── Health Check ────────────────────────────────────────────────────────────
@app.get("/api/health", tags=["System"])
async def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "service": "DAST Platform API",
        "version": "1.0.0",
    }


@app.get("/", tags=["System"])
async def root():
    """Root endpoint — API information."""
    return {
        "name": "DAST Platform",
        "description": "Dynamic Application Security Testing Platform",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/health",
    }
