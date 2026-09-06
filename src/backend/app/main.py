from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.api import v1_router

from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.api import v1_router
from app.middleware import LoggingMiddleware
from app.utils import run_seed

logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def create_tables():
    """Create all database tables if they don't exist."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    logger.info(f"🚀 {settings.APP_NAME} v1.0.0 starting up...")
    logger.info(f"🔧 Debug mode: {settings.DEBUG}")
    logger.info(f"📚 API docs: http://localhost:8000/docs")
    
    create_tables()
    
    # Seed initial data (uncomment if needed)
    # try:
    #     with SessionLocal() as db:
    #         run_seed(db)
    #     logger.info("🌱 Seed data created successfully!")
    # except Exception as e:
    #     logger.warning(f"⚠️ Seed data already exists or error: {str(e)}")
    
    logger.info(f"✅ {settings.APP_NAME} started successfully!")
    
    yield 
    
    logger.info(f"🛑 {settings.APP_NAME} shutting down...")

def create_application() -> FastAPI:
    
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        description="CampusOS - Centralized Student & Department Management Platform",
        debug=settings.DEBUG,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,  
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(LoggingMiddleware)
    
    app.include_router(v1_router, prefix=settings.API_PREFIX)
    
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": "1.0.0",
            "debug": settings.DEBUG,
        }
    
    @app.get("/")
    async def root():
        return {
            "service": settings.APP_NAME,
            "version": "1.0.0",
            "status": "running",
            "docs": "/docs" if settings.DEBUG else None,
            "api_prefix": settings.API_PREFIX,
        }
    
    return app

app = create_application()

app.include_router(v1_router, prefix=settings.API_PREFIX)