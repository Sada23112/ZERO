"""Project ZERO — Structured Logging System.

Utilizes Rich console formatting and structured logging.
"""

import sys
import logging
from typing import Optional
from rich.logging import RichHandler
from rich.console import Console

console = Console()


def setup_logger(
    name: str = "zero",
    level: str = "INFO",
    log_to_file: Optional[str] = None
) -> logging.Logger:
    """Initialize and return a configured logger with Rich console support."""
    logger = logging.getLogger(name)

    # Prevent duplicating handlers
    if logger.handlers:
        return logger

    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    # Rich Handler for Terminal Console Output
    rich_handler = RichHandler(
        console=console,
        show_time=True,
        show_path=False,
        rich_tracebacks=True,
        markup=True
    )
    rich_handler.setLevel(numeric_level)
    logger.addHandler(rich_handler)

    # File Handler if path specified
    if log_to_file:
        file_handler = logging.FileHandler(log_to_file, encoding="utf-8")
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(numeric_level)
        logger.addHandler(file_handler)

    return logger


# Default application logger
logger = setup_logger()
