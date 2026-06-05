"""Models for the Student Management System.

Core domain entities representing students, attendance records,
grades, and report cards.
"""

import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

_next_id: int = 1     # Module-level auto-increment counter


class Student:
    """Represents a student with basic identifying information.

    Attributes:
        student_id: Unique automatically assigned identifier (e.g., 'S0001').
        name: Full display name of the student.
        email: Contact email address.
        enrolled_date: Date when the student was registered (YYYY-MM-DD).
    """

    def __init__(self, name: str, email: str) -> None:
        """Initialize a new Student instance.

        Args:
            name: Full name of the student (must be non-empty).
            email: Valid email address (validated by service layer).

        Raises:
            ValueError: If name is empty or whitespace-only.
        """
        if not name.strip():
            raise ValueError("Student name cannot be empty")

        global _next_id
        self._student_id = f"S{_next_id:04d}"
        _next_id += 1

        self.name = name.strip()
        self._email = email
        self.enrolled_date = datetime.now().strftime("%Y-%m-%d")
        logger.debug(f"Created student: {self}")

    @property
    def student_id(self) -> str:
        """Access the student's unique identifier."""
        return self._student_id

    @student_id.setter
    def student_id(self, value: str) -> None:
        """Override auto-generated ID (used for data restoration)."""
        self._student_id = value

    @property
    def email(self) -> str:
        """Access student's email."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """Update the student's email address.

        Args:
            value: New email string (validation should be at service layer).
        """
        old_email = self._email
        self._email = value
        logger.info(f"Email updated for ID {self._student_id}: {old_email} -> {value}")

    def get_info(self) -> str:
        """Return a formatted string of student information.

        Returns:
            Human-readable summary with all key fields.
        """
        return (
            f"ID: {self.student_id} | Name: {self.name} "
            f"| Email: {self.email} | Enrolled: {self.enrolled_date}"
        )

    def __repr__(self) -> str:
        return f"Student(id={self._student_id!r}, name={self.name!r}, email={self._email!r})"


class Attendance:
    """Represents an attendance record for a student on a specific date.

    Attributes:
        student_id: Identifier linking to the Student entity.
        date: Date string in YYYY-MM-DD format.
        status: Either 'P' (present) or 'A' (absent).
    """

    VALID_STATUS = {"P", "A"}

    def __init__(self, student_id: str, date: Optional[str] = None, status: str = "P") -> None:
        """Initialize attendance record.

        Args:
            student_id: Target student identifier.
            date: Override for specific date (defaults to today).
            status: Attendance marker - 'P' or 'A'.

        Raises:
            ValueError: If status is not P or A.
        """
        if status.upper() not in self.VALID_STATUS:
            raise ValueError(f"Invalid status '{status}'. Must be 'P' or 'A'.")

        self.student_id = student_id.strip()
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.status = status.upper()
        logger.debug(f"Created attendance: {self}")

    def mark_present(self) -> None:
        """Update this record to present."""
        if self.status != "P":
            self.status = "P"
            logger.info(f"Attendance updated to PRESENT: {self.student_id} on {self.date}")

    def mark_absent(self) -> None:
        """Update this record to absent."""
        if self.status != "A":
            self.status = "A"
            logger.info(f"Attendance updated to ABSENT: {self.student_id} on {self.date}")

    def get_info(self) -> str:
        """Return formatted attendance info string.

        Returns:
            Human-readable attendance record summary.
        """
        return f"Student ID: {self.student_id} | Date: {self.date} | Status: {self.status}"

    def __repr__(self) -> str:
        return f"Attendance(student_id={self.student_id!r}, date={self.date!r}, status={self.status!r})"


class Grade:
    """Represents a single grade record for a student in a subject.

    Automatically clamps scores to 0-100 range and computes letter grades.

    Attributes:
        student_id: Identifier linking to the Student entity.
        subject: Course name or label.
        score: Numeric score (clamped to 0-100).
        grade: Computed letter grade based on score thresholds.
    """

    @staticmethod
    def _calculate_letter_grade(score: float) -> str:
        """Convert numeric score to letter grade.

        Grading Thresholds:
            >= 90 → A+, >= 80 → A, >= 70 → B+, >= 60 → B,
            >= 50 → C, >= 40 → D, < 40 → F

        Args:
            score: Numeric value to evaluate.

        Returns:
            Single or double character letter grade string.
        """
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B+"
        elif score >= 60:
            return "B"
        elif score >= 50:
            return "C"
        elif score >= 40:
            return "D"
        else:
            return "F"

    def __init__(self, student_id: str, subject: str, score: float) -> None:
        """Initialize a grade record with clamped score.

        Args:
            student_id: Target student identifier.
            subject: Course name (required).
            score: Numeric score (automatically clamped to 0-100).

        Raises:
            ValueError: If subject is empty.
        """
        if not subject.strip():
            raise ValueError("Subject cannot be empty")

        self.student_id = student_id.strip()
        self.subject = subject.strip()
        self.score = max(0.0, min(100.0, float(score)))
        self.grade = self._calculate_letter_grade(self.score)
        logger.debug(f"Created grade: {self}")

    def get_info(self) -> str:
        """Return formatted grade info string.

        Returns:
            Human-readable grade record summary.
        """
        return (
            f"Student ID: {self.student_id} | Subject: {self.subject} "
            f"| Score: {self.score:.1f} | Grade: {self.grade}"
        )

    def __repr__(self) -> str:
        return (
            f"Grade(student_id={self.student_id!r}, subject={self.subject!r}, "
            f"score={self.score!r}, grade={self.grade!r})"
        )


class ReportCard:
    """Aggregates grades for a single student and computes summary statistics.

    Provides formatted output suitable for display or export.

    Attributes:
        student_id: Identifier of the student this report belongs to.
        student_name: Display name of the student.
        grades: Collection of Grade objects for this student.
    """

    def __init__(self, student_id: str, student_name: str) -> None:
        """Initialize empty report card.

        Args:
            student_id: Student identifier.
            student_name: Student display name.
        """
        self.student_id = student_id
        self.student_name = student_name
        self.grades: list[Grade] = []

    def add_grade(self, grade: Grade) -> None:
        """Add a single grade to this report card.

        Args:
            grade: A properly initialized Grade instance.

        Raises:
            ValueError: If the grade's student ID doesn't match this report card.
        """
        if grade.student_id != self.student_id:
            raise ValueError(
                f"Grade belongs to {grade.student_id}, not {self.student_id}"
            )
        self.grades.append(grade)

    @property
    def average_score(self) -> float:
        """Compute average score across all grades. Returns 0 if no grades."""
        return sum(g.score for g in self.grades) / len(self.grades) if self.grades else 0.0

    @property
    def highest_score(self) -> float:
        """Compute highest individual score. Returns 0 if no grades."""
        return max(g.score for g in self.grades) if self.grades else 0.0

    @property
    def lowest_score(self) -> float:
        """Compute lowest individual score. Returns 0 if no grades."""
        return min(g.score for g in self.grades) if self.grades else 0.0

    def get_summary(self) -> str:
        """Return a formatted report card summary string.

        Includes individual grades and computed statistics.

        Returns:
            Multi-line formatted string ready for display.
        """
        lines = [
            "=" * 50,
            f"Report Card: {self.student_name} ({self.student_id})",
            "=" * 50,
        ]
        if not self.grades:
            lines.append("No grades recorded yet.")
        else:
            for i, grade in enumerate(self.grades, 1):
                lines.append(f"   {i}. {grade.subject}: {grade.score:.1f} ({grade.grade})")
            lines.append("")
            lines.append(f"Average Score    : {self.average_score:.2f}")
            lines.append(f"Highest Score    : {self.highest_score:.1f}")
            lines.append(f"Lowest Score     : {self.lowest_score:.1f}")
        lines.append("=" * 50)
        return "\n".join(lines)
