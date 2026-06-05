"""Configuration settings for Student Management System."""

from pathlib import Path

from .paths import DATA_DIR, STUDENTS_CSV, ATTENDANCE_CSV, GRADES_CSV
from .logging_config import setup_logging

__all__ = ["DATA_DIR", "STUDENTS_CSV", "ATTENDANCE_CSV", "GRADES_CSV", "setup_logging"]
