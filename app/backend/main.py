from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import uvicorn
from contextlib import asynccontextmanager
import time

from core.config import settings
from api.routes import router
from core.logging import setup_logging

# Setup colored logging
setup_logging(
    log_level="DEBUG" if settings.DEBUG_MODE else "INFO",
    log_file="logs/app.log" if not settings.DEBUG_MODE else None
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("🚀 Starting Vietnam Law Chatbot API")
    logger.info(f"🔧 Debug mode: {settings.DEBUG_MODE}")
    logger.info(f"🌐 Server will run on http://{settings.HOST}:{settings.PORT}")
    logger.info("✅ Application startup complete")
    yield
    # Shutdown
    logger.info("🛑 Shutting down Vietnam Law Chatbot API")

# Create FastAPI application
app = FastAPI(
    title="Law Chatbot API",
    description="Vietnamese Legal Document Chatbot API using Qdrant, Neo4j, and LLM",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(router, prefix="/api/v1")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "message": "An unexpected error occurred",
            "detail": str(exc) if settings.DEBUG_MODE else "Internal server error"
        }
    )


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests with colors."""
    start_time = time.time()
    
    # Log incoming request
    logger.info(f"📥 {request.method} {request.url.path} - Client: {request.client.host if request.client else 'unknown'}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # Choose emoji and log level based on status code
    if response.status_code < 300:
        emoji = "✅"
        log_level = logging.INFO
    elif response.status_code < 400:
        emoji = "🔄"
        log_level = logging.INFO
    elif response.status_code < 500:
        emoji = "⚠️"
        log_level = logging.WARNING
    else:
        emoji = "❌"
        log_level = logging.ERROR
    
    logger.log(
        log_level,
        f"📤 {emoji} {request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    
    return response


if __name__ == "__main__":
    import time
    
    # Configure uvicorn to use our logging
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG_MODE,
        log_config=None,  # Disable uvicorn's default logging config
        access_log=False,  # Disable uvicorn's access logging (we handle it in middleware)
    )
