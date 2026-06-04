"""Service layer — business logic for Student Management System."""

import csv
from datetime import datetime
from typing import Optional
from models import Student, Attendance, Grade
from repository import CSVRepository


class StudentService:
    """Manages student CRUD operations."""

    def __init__(self):
        self._repository = CSVRepository("student_data/students.csv")
        self._repository.ensure_file(["student_id", "name", "email", "enrolled_date"])
        self._students: dict[str, Student] = {}
        self._refresh()

    def _refresh(self) -> None:
        """Rebuild in-memory store from CSV."""
        self._students.clear()
        for row in self._repository.read_all():
            if len(row) >= 4:
                student = Student(name=row[1], email=row[2])
                student.student_id = row[0]    # Restore ID from CSV
                self._students[student.student_id] = student

    def add_student(self, name: str, email: str) -> Student:
        """Add a new student and return the created instance."""
        student = Student(name=name, email=email)
        self._repository.append_row([
            student.student_id, student.name, student.email, student.enrolled_date
        ])
        self._students[student.student_id] = student
        print(f"  ✓ Student added: {student}")
        return student

    def get_student(self, student_id: str) -> Optional[Student]:
        return self._students.get(student_id)

    def get_all_students(self) -> list[Student]:
        return list(self._students.values())

    def find_by_name(self, name: str) -> list[Student]:
        return [s for s in self._students.values() if name.lower() in s.name.lower()]

    def update_email(self, student_id: str, new_email: str) -> bool:
        """Update email for a student. Returns True if found & updated."""
        student = self._students.get(student_id)
        if not student:
            return False
        old_email = student.email
        student.email = new_email
        # Update CSV
        rows = self._repository.read_all()
        with open(self._repository.filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "name", "email", "enrolled_date"])
            for row in rows:
                if row[0] == student_id and len(row) >= 4:
                    writer.writerow([student_id, student.name, new_email, row[3]])
                else:
                    writer.writerow(row)
        print(f"  ✓ Email updated for {student.name}")
        return True

    def delete_student(self, student_id: str) -> bool:
        """Delete a student by ID. Returns True if found & deleted."""
        if student_id not in self._students:
            return False
        del self._students[student_id]
         # Rewrite CSV without the deleted student
        rows = self._repository.read_all()
        with open(self._repository.filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "name", "email", "enrolled_date"])
            for row in rows:
                if row[0] != student_id:
                    writer.writerow(row)
        print(f"  ✓ Student deleted: {student_id}")
        return True

    def count(self) -> int:
        return len(self._students)


class AttendanceService:
    """Manages attendance tracking."""

    def __init__(self, student_service: StudentService):
        self._repository = CSVRepository("student_data/attendance.csv")
        self._repository.ensure_file(["student_id", "date", "status"])
        self._student_service = student_service
        self._records: list[dict] = []
        self._refresh()

    def _refresh(self) -> None:
        self._records.clear()
        for row in self._repository.read_all():
            if len(row) >= 3:
                self._records.append({
                    "student_id": row[0],
                    "date": row[1],
                    "status": row[2],
                })

    def mark_attendance(self, student_id: str, status: str = "P") -> Optional[str]:
        """Mark attendance for a student. Returns message or None."""
        if not self._student_service.get_student(student_id):
            return f"  ✗ Student '{student_id}' not found."

        today = datetime.now().strftime("%Y-%m-%d")

         # Check duplicate for same day
        for record in self._records:
            if record["student_id"] == student_id and record["date"] == today:
                return f"  ✗ Attendance already marked for {student_id} on {today}."

        attendance = Attendance(student_id=student_id, date=today, status=status)
        self._repository.append_row([student_id, today, status.upper()])
        self._records.append({
            "student_id": student_id,
            "date": today,
            "status": status.upper(),
        })
        return f"  ✓ Attendance marked: {student_id} → {status.upper()} on {today}"

    def get_attendance(self, student_id: str) -> list[dict]:
        """Get all attendance records for a student."""
        return [r for r in self._records if r["student_id"] == student_id]

    def get_all_records(self) -> list[dict]:
        return self._records

    def get_summary(self) -> dict:
        """Return summary statistics."""
        present = sum(1 for r in self._records if r["status"] == "P")
        absent = sum(1 for r in self._records if r["status"] == "A")
        return {"total": len(self._records), "present": present, "absent": absent}


class GradeService:
    """Manages grades and report cards."""

    def __init__(self, student_service: StudentService):
        self._repository = CSVRepository("student_data/grades.csv")
        self._repository.ensure_file(["student_id", "subject", "score", "grade"])
        self._student_service = student_service
        self._grades: list[dict] = []
        self._refresh()

    def _refresh(self) -> None:
        self._grades.clear()
        for row in self._repository.read_all():
            if len(row) >= 4:
                self._grades.append({
                    "student_id": row[0],
                    "subject": row[1],
                    "score": float(row[2]),
                    "grade": row[3],
                })

    def add_grade(self, student_id: str, subject: str, score: float) -> Optional[str]:
        """Add a grade for a student. Returns message or None."""
        if not self._student_service.get_student(student_id):
            return f"  ✗ Student '{student_id}' not found."

        letter = Grade._calculate_letter_grade(score)
        record = {"student_id": student_id, "subject": subject, "score": score, "grade": letter}
        self._repository.append_row([student_id, subject, str(score), letter])
        self._grades.append(record)
        return f"  ✓ Grade '{letter}' recorded for {student_id} in {subject} (Score: {score})"

    def get_grades(self, student_id: str) -> list[dict]:
        """Get all grades for a student."""
        return [g for g in self._grades if g["student_id"] == student_id]

    def get_all_grades(self) -> list[dict]:
        return self._grades

    def get_report_card(self, student_id: str) -> Optional[str]:
        """Generate a formatted report card for a student."""
        student = self._student_service.get_student(student_id)
        if not student:
            return None

        grades = self.get_grades(student_id)
        if not grades:
            return (
                f"  Report Card: {student.name} ({student_id})\n"
                "  No grades recorded yet.\n" + "=" * 50
            )

        scores = [g["score"] for g in grades]
        average = sum(scores) / len(scores)
        highest = max(scores)
        lowest = min(scores)

        lines = [
             "=" * 50,
            f"  Report Card: {student.name} ({student_id})",
             "=" * 50,
         ]
        for i, grade in enumerate(grades, 1):
            lines.append(f"   {i}. {grade['subject']}: {grade['score']:.1f} ({grade['grade']})")
        lines.append("")
        lines.append(f"  Average Score : {average:.2f}")
        lines.append(f"  Highest Score : {highest:.1f}")
        lines.append(f"  Lowest Score   : {lowest:.1f}")
        lines.append("=" * 50)
        return "\n".join(lines)

    def get_summary(self) -> dict:
        """Return overall grade statistics."""
        return {"total_grades": len(self._grades), "all_grades": self._grades}
