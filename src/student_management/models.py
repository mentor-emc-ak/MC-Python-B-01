"""Models for the Student Management System."""

from datetime import datetime


class Student:
    """Represents a student with basic information."""

    _next_id = 1  # Auto-increment counter

    def __init__(self, name: str, email: str):
        self.student_id = f"S{Student._next_id:04d}"
        Student._next_id += 1
        self.name = name
        self.email = email
        self.enrolled_date = datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def greeting() -> str:
        return "Welcome to the Student Management System!"

    @property
    def student_id(self) -> str:
        return self._student_id

    @student_id.setter
    def student_id(self, value: str):
        self._student_id = value

    def update_email(self, new_email: str) -> None:
        """Update the student's email address."""
        old_email = self.email
        self.email = new_email
        print(f"  Email updated: {old_email} → {new_email}")

    def get_info(self) -> str:
        """Return a formatted string of student information."""
        return (
            f"ID: {self.student_id} | Name: {self.name} "
            f"| Email: {self.email} | Enrolled: {self.enrolled_date}"
        )

    def __repr__(self) -> str:
        return f"Student(id={self.student_id}, name='{self.name}', email='{self.email}')"


class Attendance:
    """Represents an attendance record for a student on a specific date."""

    def __init__(self, student_id: str, date: str = None, status: str = "P"):
        self.student_id = student_id
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.status = status.upper() if status in ("P", "A") else "A"

    def mark_present(self) -> None:
        self.status = "P"

    def mark_absent(self) -> None:
        self.status = "A"

    def get_info(self) -> str:
        return f"Student ID: {self.student_id} | Date: {self.date} | Status: {self.status}"

    def __repr__(self) -> str:
        return f"Attendance(student_id={self.student_id}, date='{self.date}', status='{self.status}')"


class Grade:
    """Represents a grade record for a student in a subject."""

    def __init__(self, student_id: str, subject: str, score: float):
        self.student_id = student_id
        self.subject = subject
        self.score = max(0, min(100, score))  # Clamp between 0-100
        self.grade = self._calculate_letter_grade(self.score)

    @staticmethod
    def _calculate_letter_grade(score: float) -> str:
        """Convert numeric score to letter grade."""
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

    def get_info(self) -> str:
        return (
            f"Student ID: {self.student_id} | Subject: {self.subject} "
            f"| Score: {self.score:.1f} | Grade: {self.grade}"
        )

    def __repr__(self) -> str:
        return f"Grade(student_id={self.student_id}, subject='{self.subject}', score={self.score}, grade='{self.grade}')"


class ReportCard:
    """Aggregates grades for a single student and computes summary statistics."""

    def __init__(self, student_id: str, student_name: str):
        self.student_id = student_id
        self.student_name = student_name
        self.grades: list[Grade] = []

    def add_grade(self, grade: Grade) -> None:
        self.grades.append(grade)

    @property
    def average_score(self) -> float:
        if not self.grades:
            return 0.0
        return sum(g.score for g in self.grades) / len(self.grades)

    @property
    def highest_score(self) -> float:
        if not self.grades:
            return 0.0
        return max(g.score for g in self.grades)

    @property
    def lowest_score(self) -> float:
        if not self.grades:
            return 0.0
        return min(g.score for g in self.grades)

    def get_summary(self) -> str:
        """Return a formatted report card summary."""
        lines = [
            "=" * 50,
            f"  Report Card: {self.student_name} ({self.student_id})",
            "=" * 50,
        ]
        if not self.grades:
            lines.append("  No grades recorded yet.")
        else:
            for i, grade in enumerate(self.grades, 1):
                lines.append(f"  {i}. {grade.subject}: {grade.score:.1f} ({grade.grade})")
            lines.append("")
            lines.append(f"  Average Score : {self.average_score:.2f}")
            lines.append(f"  Highest Score : {self.highest_score:.1f}")
            lines.append(f"  Lowest Score  : {self.lowest_score:.1f}")
        lines.append("=" * 50)
        return "\n".join(lines)
