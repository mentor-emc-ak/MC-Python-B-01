"""File path configuration for the Student Management System."""

from pathlib import Path


def _get_data_dir() -> Path:
     """Get or create the data directory. Can be overridden via DATA_DIR env var."""
     import os
     default = Path(__file__).resolve().parent.parent.parent / ".." / "data"
     return Path(os.environ.get("DATA_DIR", str(default))).resolve()


DATA_DIR = _get_data_dir()
STUDENTS_CSV = DATA_DIR / "students.csv"
ATTENDANCE_CSV = DATA_DIR / "attendance.csv"
GRADES_CSV = DATA_DIR / "grades.csv"
