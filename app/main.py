"""FastAPI main application"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils import settings, setup_logging
from app.engine import EventQueue
from app.events import EventType

# Setup logging
setup_logging("INFO")
logger = logging.getLogger(__name__)

# Global event queue
event_queue: EventQueue = EventQueue()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown"""
    # Startup
    logger.info("🚀 Algo Trading Platform starting...")
    logger.info(f"Environment: {settings.DEBUG and 'DEBUG' or 'PRODUCTION'}")
    yield
    # Shutdown
    logger.info("🛑 Shutting down gracefully...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": settings.APP_VERSION,
        "event_queue_size": event_queue.size(),
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Algo Trading Platform",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
