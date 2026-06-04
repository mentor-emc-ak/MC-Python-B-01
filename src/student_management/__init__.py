"""Student Management System Package."""

from .models import Student, Attendance, Grades
from .service import StudentService
from .repository import StudentRepository

__version__ = "0.1.0"
