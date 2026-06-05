"""Logging configuration for the Student Management System."""

import logging
from pathlib import Path


def setup_logging(level: int = logging.INFO, log_file: Path | None = None) -> logging.Logger:
      """Configure and return a logger instance.

     Args:
         level: Logging level (default: INFO)
         log_file: Optional file path for file-based logging

     Returns:
         Configured Logger instance
     """
     logger = logging.getLogger("student_management")
     logger.setLevel(level)

    # Avoid adding duplicate handlers
     if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
     )

    # Console handler
     console_handler = logging.StreamHandler()
     console_handler.setFormatter(formatter)
     logger.addHandler(console_handler)

    # File handler (optional)
     if log_file:
        file_handler = logging.FileHandler(str(log_file))
        file_handler.setFormatter(formatter)
         logger.addHandler(file_handler)

    return logger
