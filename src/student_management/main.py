"""Student Management System — Main CLI Entry Point."""

from models import Student
from service import StudentService, AttendanceService, GradeService


def print_header(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print("=" * 50)


def print_separator() -> None:
    print("\n" + "-" * 50 + "\n")


def menu() -> str:
    """Display the main menu and return user's choice."""
    print("\n" + "=" * 50)
    print("   STUDENT MANAGEMENT SYSTEM")
    print("=" * 50)
    print("  1. Add Student")
    print("  2. View All Students")
    print("  3. Update Student Email")
    print("  4. Delete Student")
    print("  5. Mark Attendance")
    print("  6. View Attendance Records")
    print("  7. Add Grade")
    print("  8. View Report Card")
    print("  9. View All Grades")
    print(" 10. Show Summary Report")
    print("  0. Exit")
    print("=" * 50)
    return input("\nEnter your choice: ").strip()


def add_student(student_service: StudentService) -> None:
    name = input("   Enter student name: ").strip()
    email = input("   Enter student email: ").strip()
    if not name or not email:
        print("   ✗ Name and email are required!")
        return
    student_service.add_student(name, email)


def view_students(student_service: StudentService) -> None:
    students = student_service.get_all_students()
    if not students:
        print("   No students registered yet.")
        return
    print(f"\n   {'ID':<8} {'Name':<20} {'Email':<25} {'Enrolled'}")
    print("   " + "-" * 65)
    for s in students:
        print(f"   {s.student_id:<8} {s.name:<20} {s.email:<25} {s.enrolled_date}")
    print(f"\n   Total: {len(students)} student(s)")


def update_email(student_service: StudentService) -> None:
    students = student_service.get_all_students()
    if not students:
        print("   No students registered yet.")
        return
    print("   Available students:")
    for s in students:
        print(f"     {s.student_id} - {s.name}")
    student_id = input("   Enter Student ID: ").strip()
    new_email = input("   Enter new email: ").strip()
    if not new_email:
        print("   ✗ Email cannot be empty!")
        return
    if student_service.update_email(student_id, new_email):
        print(f"   ✓ Email updated for {student_id}")
    else:
        print(f"   ✗ Student '{student_id}' not found.")


def delete_student(student_service: StudentService) -> None:
    students = student_service.get_all_students()
    if not students:
        print("   No students registered yet.")
        return
    student_id = input("   Enter Student ID to delete: ").strip()
    if student_service.delete_student(student_id):
        print(f"   ✓ Student '{student_id}' deleted successfully.")
    else:
        print(f"   ✗ Student '{student_id}' not found.")


def mark_attendance(
    attendance_service: AttendanceService, student_service: StudentService
) -> None:
    students = student_service.get_all_students()
    if not students:
        print("   No students registered. Add students first!")
        return
    print("   Registered Students:")
    for s in students:
        print(f"     {s.student_id} - {s.name}")
    student_id = input("   Enter Student ID: ").strip()
    status = input("   Mark attendance (P/A) [default P]: ").strip().upper() or "P"
    if status not in ("P", "A"):
        status = "P"
    result = attendance_service.mark_attendance(student_id, status)
    if result:
        print(result)


def view_attendance(attendance_service: AttendanceService) -> None:
    records = attendance_service.get_all_records()
    if not records:
        print("   No attendance records found.")
        return
    print(f"\n   {'Student ID':<10} {'Date':<15} {'Status'}")
    print("   " + "-" * 40)
    for r in records:
        print(f"   {r['student_id']:<10} {r['date']:<15} {r['status']}")


def add_grade(grade_service: GradeService, student_service: StudentService) -> None:
    students = student_service.get_all_students()
    if not students:
        print("   No students registered. Add students first!")
        return
    print("   Available Students:")
    for s in students:
        print(f"     {s.student_id} - {s.name}")
    student_id = input("   Enter Student ID: ").strip()
    subject = input("   Enter Subject: ").strip()
    try:
        score = float(input("   Enter Score (0-100): ").strip())
        if not 0 <= score <= 100:
            print("   ✗ Score out of range. Defaulting to 0.")
            score = 0
    except ValueError:
        print("   ✗ Invalid score. Defaulting to 0.")
        score = 0.0
    result = grade_service.add_grade(student_id, subject, score)
    if result:
        print(result)


def view_report_card(
    grade_service: GradeService, student_service: StudentService
) -> None:
    students = student_service.get_all_students()
    if not students:
        print("   No students registered.")
        return
    print("   Available Students:")
    for s in students:
        print(f"     {s.student_id} - {s.name}")
    student_id = input("   Enter Student ID: ").strip()
    card = grade_service.get_report_card(student_id)
    if card:
        print(card)
    else:
        print(f"   ✗ Student '{student_id}' not found.")


def view_all_grades(grade_service: GradeService) -> None:
    grades = grade_service.get_all_grades()
    if not grades:
        print("   No grades recorded yet.")
        return
    print(f"\n   {'Student ID':<10} {'Subject':<15} {'Score':<8} {'Grade'}")
    print("   " + "-" * 50)
    for g in grades:
        print(
            f"   {g['student_id']:<10} {g['subject']:<15} {g['score']:<8.1f} {g['grade']}"
        )


def show_summary(
    student_service: StudentService,
    attendance_service: AttendanceService,
    grade_service: GradeService,
) -> None:
    students = student_service.get_all_students()
    att_summary = attendance_service.get_summary()
    grade_summary = grade_service.get_summary()

    print("\n" + "=" * 50)
    print("         SUMMARY REPORT")
    print("=" * 50)
    print(f"   Total Students Registered : {len(students)}")
    print(f"   Attendance Records        : {att_summary['total']}")
    print(f"     - Present               : {att_summary['present']}")
    print(f"     - Absent                : {att_summary['absent']}")
    print(f"   Grades Recorded           : {grade_summary['total_grades']}")
    print("=" * 50)


def main() -> None:
    """Main entry point for the Student Management System."""
    print(Student.greeting())

    # Initialize services
    student_service = StudentService()
    attendance_service = AttendanceService(student_service)
    grade_service = GradeService(student_service)

    while True:
        choice = menu()

        if choice == "1":
            add_student(student_service)
        elif choice == "2":
            view_students(student_service)
        elif choice == "3":
            update_email(student_service)
        elif choice == "4":
            delete_student(student_service)
        elif choice == "5":
            mark_attendance(attendance_service, student_service)
        elif choice == "6":
            view_attendance(attendance_service)
        elif choice == "7":
            add_grade(grade_service, student_service)
        elif choice == "8":
            view_report_card(grade_service, student_service)
        elif choice == "9":
            view_all_grades(grade_service)
        elif choice == "10":
            show_summary(student_service, attendance_service, grade_service)
        elif choice == "0":
            print("\n   Goodbye! Thank you for using Student Management System.")
            break
        else:
            print("   ✗ Invalid choice. Please enter a number from 0 to 10.")


if __name__ == "__main__":
    main()
