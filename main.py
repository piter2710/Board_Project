from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings import settings
import logging
from database import engine, Base
import models
from routes.board import router as board_router
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up FastAPI application...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    logger.info("Shutting down FastAPI application...")
    await engine.dispose()
    
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

# Set CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}

# Include routing
# from routes.my_router import router 
# app.include_router(router, prefix=settings.API_V1_PREFIX)
app.include_router(board_router)
