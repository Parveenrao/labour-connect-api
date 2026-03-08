import sys
import os
from pathlib import Path
from loguru import logger
from app.core.config import settings


def setup_logging() -> None:
    """Configure application logging."""

    logger.remove()

    # -----------------------------------
    # Console Logging (works everywhere)
    # -----------------------------------
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        colorize=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
    )

    # -----------------------------------
    # Skip file logging on Vercel
    # -----------------------------------
    if os.getenv("VERCEL") != "1":

        LOG_DIR = Path("logs")
        LOG_DIR.mkdir(exist_ok=True)

        logger.add(
            LOG_DIR / "app_{time:YYYY-MM-DD}.log",
            level="INFO",
            rotation="00:00",
            retention=f"{settings.LOG_RETENTION_DAYS} days",
            compression="zip",
            enqueue=True,
        )

        logger.add(
            LOG_DIR / "errors_{time:YYYY-MM-DD}.log",
            level="ERROR",
            rotation="00:00",
            retention=f"{settings.LOG_ERROR_RETENTION_DAYS} days",
            compression="zip",
            enqueue=True,
        )

    logger.info(
        "Logging initialized | ENV=%s | LEVEL=%s",
        settings.APP_ENV,
        settings.LOG_LEVEL,
    )