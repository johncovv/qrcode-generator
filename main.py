from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging


from core import settings
from routes import generator_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Starting up the application...")
    logger.info(f"Environment: {settings.environment}")
    yield
    # Shutdown actions
    logger.info("Shutting down the application...")


app = FastAPI(
    title="My QR Code Generator API",
    description="An API to generate QR codes with optional embedded images and store them in S3.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(generator_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.is_development,
        log_level="info",
    )
