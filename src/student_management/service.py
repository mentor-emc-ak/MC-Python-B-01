"""Service layer — business logic for Student Management System.

This module implements the service layer which orchestrates models and repositories.
It handles validation, business rules, and transactional consistency.

Usage:
     from student_management import StudentService
     svc = StudentService()
     svc.add_student("John Doe", "john@example.com")
"""

import logging
from datetime import datetime
from typing import Optional

from .models import Student, Attendance, Grade
from .repository import CSVRepository
from .config import STUDENTS_CSV, ATTENDANCE_CSV, GRADES_CSV

logger = logging.getLogger(__name__)


class StudentService:
        """Manages student CRUD operations and persistence.

     Wraps Student models with CSV-based persistence via CSVRepository.
     All public methods validate inputs and log outcomes.
       """

    STUDENT_HEADERS = ["student_id", "name", "email", "enrolled_date"]

    def __init__(self) -> None:
        self._repository = CSVRepository(STUDENTS_CSV)
        self._repository.ensure_file(self.STUDENT_HEADERS)
         self._students: dict[str, Student] = {}
         self._refresh()
        logger.info("StudentService initialized")

    def _refresh(self) -> None:
        """Rebuild in-memory store from CSV data.

     Reads all student records and repopulates the _students dictionary.
     Used on initialization and after bulk operations.
       """
     self._students.clear()
     rows = self._repository.read_all()
     for row in rows:
         if len(row) >= 4:
             try:
                student = Student(student_id=row[0], name=row[1], email=row[2])
                self._students[student.student_id] = student
         except ValueError as e:
              logger.warning(f"Skipping invalid row {row}: {e}")

    def validate_email(self, email: str) -> bool:
        """Validate basic email format.

     Args:
         email: Email address to validate.

     Returns:
         True if email contains '@' and has valid structure.
       """
    if "@" not in email or "." not in email.split("@")[-1]:
         logger.warning(f"Invalid email format: {email}")
         return False
      return True

    def add_student(self, name: str, email: str) -> Optional[Student]:
        """Add a new student and persist to CSV.

     Args:
         name: Full name of the student.
         email: Valid email address.

     Returns:
         Created Student instance, or None if validation fails.
       """
    if not name.strip():
         logger.warning("Student name cannot be empty")
        return None
     if not self.validate_email(email):
          logger.warning(f"Invalid email format provided: {email}")
          return None

     student = Student(name=name, email=email)
     self._repository.append_row([
          student.student_id, student.name, student.email, student.enrolled_date
      ])
     self._students[student.student_id] = student
        logger.info(f"Student added: {student}")
        return student

    def get_student(self, student_id: str) -> Optional[Student]:
        """Retrieve a student by their unique ID.

     Args:
          student_id: The student's unique identifier.

     Returns:
         Student object if found, None otherwise.
       """
     return self._students.get(student_id)

    def get_all_students(self) -> list[Student]:
        """Retrieve all registered students.

     Returns:
         List of all Student objects currently in memory.
       """
     return list(self._students.values())

    def find_by_name(self, name: str) -> list[Student]:
        """Search students by partial name match (case-insensitive).

     Args:
         name: Substring to search against student names.

     Returns:
         List of matching Student objects.
       """
    return [s for s in self._students.values() if name.lower() in s.name.lower()]

    def update_email(self, student_id: str, new_email: str) -> bool:
        """Update the email address for an existing student.

     Validates the new email and updates both memory and CSV storage.

     Args:
         student_id: Target student identifier.
         new_email: New valid email address.

     Returns:
             True if update succeeded, False if student not found or invalid email.
       """
    student = self._students.get(student_id)
     if not student:
        logger.warning(f"Student {student_id} not found for email update")
         return False

     if not self.validate_email(new_email):
          logger.warning(f"Invalid email format for update: {new_email}")
          return False

      # Update in memory
     old_email = student.email
     student._email = new_email   # Private attribute to bypass property side effects
      # Update CSV using repository (delegated, no direct file access)
     row_data = [student_id, student.name, new_email, student.enrolled_date]
        updated = self._repository.update_row(0, student_id, row_data)

          if updated:
          logger.info(f"Email updated for {student.name}: {old_email} -> {new_email}")
       return True
      return False

    def delete_student(self, student_id: str) -> bool:
         """Delete a student by ID from memory and CSV storage.

     Args:
         student_id: Identifier of the student to remove.

     Returns:
         True if deletion succeeded, False if student was not found.
       """
    if student_id not in self._students:
        logger.warning(f"Cannot delete non-existent student: {student_id}")
         return False

      del self._students[student_id]
          # Update CSV using repository
     headers = self._repository.read_header()
      rows = [r for r in self._repository.read_all() if r[0] != student_id]
        self._repository.write_all(headers, rows)
         logger.info(f"Student deleted: {student_id}")
        return True

    def count(self) -> int:
        """Count currently registered students.

     Returns:
         Number of students in memory.
       """
    return len(self._students)


class AttendanceService:
      """Manages attendance tracking and validation.

     Prevents duplicate daily attendance records and validates student existence
     before marking attendance.
       """

    ATTENDANCE_HEADERS = ["student_id", "date", "status"]

    def __init__(self, student_service: StudentService) -> None:
        self._repository = CSVRepository(ATTENDANCE_CSV)
         self._repository.ensure_file(self.ATTENDANCE_HEADERS)
         self._student_service = student_service
          self._records: list[dict] = []
          self._refresh()
        logger.info("AttendanceService initialized")

    def _refresh(self) -> None:
        """Rebuild in-memory attendance records from CSV."""
     self._records.clear()
     for row in self._repository.read_all():
         if len(row) >= 3:
             self._records.append({
                "student_id": row[0],
                "date": row[1],
                 "status": row[2],
           })

    def mark_attendance(
             self, student_id: str, date: Optional[str] = None, status: str = "P"
     ) -> Optional[str]:
        """Mark attendance for a validated student on a specific date.

     Prevents duplicate marks for the same student on the same day.

     Args:
         student_id: Target student identifier.
         date: Date string in YYYY-MM-DD format (defaults to today).
          status: Attendance status - 'P' for present, 'A' for absent.

     Returns:
         Success or error message string, None if completely invalid input.
       """
    if not self._student_service.get_student(student_id):
        msg = f"Student '{student_id}' not found."
         logger.error(msg)
        return msg

      target_date = date or datetime.now().strftime("%Y-%m-%d")
        status = "P" if status.upper() == "P" else "A"

          # Check for duplicate entry (same student, same day)
     for record in self._records:
            if record["student_id"] == student_id and record["date"] == target_date:
             msg = f"Attendance already marked for {student_id} on {target_date}."
              logger.warning(msg)
              return msg

        attendance = Attendance(student_id=student_id, date=target_date, status=status)
         self._repository.append_row([student_id, target_date, status.upper()])
      self._records.append({
             "student_id": student_id,
            "date": target_date,
               "status": status.upper(),
       })
    msg = f"Attendance marked: {student_id} → {status.upper()} on {target_date}"
          logger.info(msg)
         return msg

    def get_attendance(self, student_id: str) -> list[dict]:
       """Retrieve all attendance records for a specific student.

     Args:
         student_id: Student identifier to filter records.

     Returns:
        List of attendance record dictionaries.
      """
     return [r for r in self._records if r["student_id"] == student_id]

    def get_all_records(self) -> list[dict]:
          """Retrieve all attendance records across all students.

     Returns:
         Full list of attendance record dictionaries.
       """
     return list(self._records)

    def get_summary(self) -> dict[str, int]:
        """Calculate aggregate attendance statistics.

     Returns:
         Dictionary with 'total', 'present', and 'absent' counts.
       """
     present = sum(1 for r in self._records if r["status"] == "P")
     absent = sum(1 for r in self._records if r["status"] == "A")
          return {"total": len(self._records), "present": present, "absent": absent}


class GradeService:
      """Manages academic grades and report card generation.

     Validates student existence before recording grades and computes
     summary statistics for report cards.
       """

    GRADE_HEADERS = ["student_id", "subject", "score", "grade"]

    def __init__(self, student_service: StudentService) -> None:
        self._repository = CSVRepository(GRADES_CSV)
        self._repository.ensure_file(self.GRADE_HEADERS)
        self._student_service = student_service
         self._grades: list[dict] = []
           self._refresh()
          logger.info("GradeService initialized")

    def _refresh(self) -> None:
         """Rebuild in-memory grade records from CSV."""
     self._grades.clear()
      for row in self._repository.read_all():
        if len(row) >= 4:
                try:
                    self._grades.append({
                         "student_id": row[0],
                      "subject": row[1],
                         "score": float(row[2]),
                        "grade": row[3],
                  })
              except ValueError as e:
                   logger.warning(f"Skipping invalid grade row {row}: {e}")

    def add_grade(
          self, student_id: str, subject: str, score: float
   ) -> Optional[str]:
        """Record a grade for a validated student and subject.

     Score is clamped to 0-100 range automatically.

     Args:
         student_id: Target student identifier.
          subject: Course/subject name.
         score: Numeric score (clamped to 0-100).

     Returns:
         Success message string, or error if student not found.
       """
     if not self._student_service.get_student(student_id):
         msg = f"Student '{student_id}' not found."
          logger.error(msg)
         return msg

     score = max(0.0, min(100.0, float(score)))
     letter = Grade._calculate_letter_grade(score)
     record = {
           "student_id": student_id,
             "subject": subject,
            "score": score,
               "grade": letter,
       }
      self._repository.append_row([student_id, subject, str(score), letter])
          self._grades.append(record)
        msg = f"Grade '{letter}' recorded for {student_id} in {subject} (Score: {score:.1f})"
      logger.info(msg)
       return msg

    def get_grades(self, student_id: str) -> list[dict]:
        """Retrieve all grades for a specific student.

     Args:
         student_id: Student identifier to filter records.

     Returns:
         List of grade record dictionaries.
       """
      return [g for g in self._grades if g["student_id"] == student_id]

    def get_all_grades(self) -> list[dict]:
       """Retrieve all grade records across all students.

     Returns:
        Complete list of grade dictionaries.
      """
      return list(self._grades)

    def get_report_card(self, student_id: str) -> Optional[str]:
          """Generate a formatted report card for a student.

      Computes average, highest, and lowest scores across all subjects.

     Args:
         student_id: Student identifier.

     Returns:
         Formatted report card string, or error message if student not found/no grades.
       """
     student = self._student_service.get_student(student_id)
      if not student:
            msg = f"Student '{student_id}' not found."
             logger.error(msg)
          return msg

        grades = self.get_grades(student_id)
         if not grades:
              return self._format_empty_report(student.name, student_id)

        scores = [g["score"] for g in grades]
        average = sum(scores) / len(scores)
         highest = max(scores)
          lowest = min(scores)

          lines = [
               "=" * 50,
            f"Report Card: {student.name} ({student_id})",
              "=" * 50,
           ]
         for i, grade in enumerate(grades, 1):
            lines.append(f"  {i}. {grade['subject']}: {grade['score']:.1f} ({grade['grade']})")
          lines.append("")
           lines.append(f"Average Score  : {average:.2f}")
             lines.append(f"Highest Score  : {highest:.1f}")
              lines.append(f"Lowest Score   : {lowest:.1f}")
            lines.append("=" * 50)

         logger.info(f"Generated report card for {student_id}")
          return "\n".join(lines)

    def _format_empty_report(self, name: str, student_id: str) -> str:
        """Format a report card with no grades yet recorded.

     Args:
        name: Student display name.
         student_id: Student identifier.

     Returns:
         Formatted empty report card string.
       """
     return (
            "  Report Card: {name} ({student_id})\n"
             "  No grades recorded yet.\n" + "=" * 50
      ).format(name=name, student_id=student_id)

    def get_summary(self) -> dict[str, object]:
        """Calculate overall grade statistics.

     Returns:
         Dictionary with 'total_grades' count and 'all_grades' list.
       """
     return {"total_grades": len(self._grades), "all_grades": self._grades}
