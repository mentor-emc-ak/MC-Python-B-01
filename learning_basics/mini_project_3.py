import csv
import os
from datetime import datetime


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_DIR = "student_data"
STUDENTS_CSV = os.path.join(DATA_DIR, "students.csv")
ATTENDANCE_CSV = os.path.join(DATA_DIR, "attendance.csv")
GRADES_CSV = os.path.join(DATA_DIR, "grades.csv")


# ---------------------------------------------------------------------------
# File helpers — create directories & CSV headers if missing
# ---------------------------------------------------------------------------

def ensure_data_dir():
    """Create the data directory if it does not exist."""
    os.makedirs(DATA_DIR, exist_ok=True)


def write_csv(filepath, headers, rows):
    """Write *rows* (list of lists) to a CSV file with *headers*."""
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def append_csv(filepath, row):
    """Append a single row (list) to a CSV file. Creates headers if new."""
    create_headers = not os.path.exists(filepath)
    with open(filepath, "a", newline="") as f:
        writer = csv.writer(f)
        if create_headers:
            if filepath == STUDENTS_CSV:
                writer.writerow(["student_id", "name", "email", "enrolled_date"])
            elif filepath == ATTENDANCE_CSV:
                writer.writerow(["student_id", "date", "status"])
            elif filepath == GRADES_CSV:
                writer.writerow(["student_id", "subject", "score", "grade"])
        writer.writerow(row)


def read_csv(filepath):
    """Read a CSV file and return (headers, rows). Each row is a list of strings."""
    if not os.path.exists(filepath):
        return [], []
    with open(filepath, "r", newline="") as f:
        reader = csv.reader(f)
        headers = next(reader, [])
        rows = [row for row in reader]
    return headers, rows


# ---------------------------------------------------------------------------
# Student Management
# ---------------------------------------------------------------------------

def add_student():
    """Add a new student record to students.csv."""
    student_id = input("Enter Student ID: ").strip()
    name = input("Enter Name: ").strip()
    email = input("Enter Email: ").strip()

    append_csv(STUDENTS_CSV, [student_id, name, email, datetime.now().strftime("%Y-%m-%d")])
    print(f"Student '{name}' (ID: {student_id}) added successfully.")


def view_students():
    """Display all students from students.csv."""
    headers, rows = read_csv(STUDENTS_CSV)
    if not rows:
        print("No students registered yet.")
        return

    print(f"\n{'ID':<10} {'Name':<15} {'Email':<25} {'Enrolled Date'}")
    print("-" * 70)
    for row in rows:
        if len(row) >= 4:
            print(f"{row[0]:<10} {row[1]:<15} {row[2]:<25} {row[3]}")


# ---------------------------------------------------------------------------
# Attendance Tracking
# ---------------------------------------------------------------------------

def mark_attendance():
    """Record attendance for a student on today's date."""
    headers, rows = read_csv(STUDENTS_CSV)
    if not rows:
        print("No students registered. Add students first.")
        return

    print("Registered Students:")
    for row in rows:
        if len(row) >= 2:
            print(f"  {row[0]} - {row[1]}")

    student_id = input("Enter Student ID: ").strip()

    # Check if already marked today
    today = datetime.now().strftime("%Y-%m-%d")
    _, att_rows = read_csv(ATTENDANCE_CSV)
    for row in att_rows:
        if len(row) >= 3 and row[0] == student_id and row[1] == today:
            print("Attendance already marked for today.")
            return

    status = input("Mark attendance (P/A): ").strip().upper()
    if status not in ("P", "A"):
        print("Invalid choice. Marked as Absent by default.")
        status = "A"

    append_csv(ATTENDANCE_CSV, [student_id, today, status])
    print(f"Attendance marked for {student_id}: {status}")


def view_attendance():
    """Display all attendance records."""
    headers, rows = read_csv(ATTENDANCE_CSV)
    if not rows:
        print("No attendance records found.")
        return

    print(f"\n{'Student ID':<12} {'Date':<15} {'Status'}")
    print("-" * 45)
    for row in rows:
        if len(row) >= 3:
            print(f"{row[0]:<12} {row[1]:<15} {row[2]}")


# ---------------------------------------------------------------------------
# Grades Management
# ---------------------------------------------------------------------------

def add_grade():
    """Record a grade for a student."""
    headers, rows = read_csv(STUDENTS_CSV)
    if not rows:
        print("No students registered. Add students first.")
        return

    student_id = input(f"Enter Student ID (Options: {[r[0] for r in rows]}): ").strip()

    subject = input("Enter Subject: ").strip()
    try:
        score = float(input("Enter Score (0-100): ").strip())
        if not 0 <= score <= 100:
            print("Score out of range. Defaulting to 0.")
            score = 0
    except ValueError:
        print("Invalid score. Defaulting to 0.")
        score = 0

    # Auto-grade
    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B+"
    elif score >= 60:
        grade = "B"
    elif score >= 50:
        grade = "C"
    elif score >= 40:
        grade = "D"
    else:
        grade = "F"

    append_csv(GRADES_CSV, [student_id, subject, str(score), grade])
    print(f"Grade '{grade}' recorded for {student_id} in {subject}.")


def view_grades():
    """Display all grades."""
    headers, rows = read_csv(GRADES_CSV)
    if not rows:
        print("No grades recorded yet.")
        return

    print(f"\n{'Student ID':<12} {'Subject':<15} {'Score':<8} {'Grade'}")
    print("-" * 55)
    for row in rows:
        if len(row) >= 4:
            print(f"{row[0]:<12} {row[1]:<15} {row[2]:<8} {row[3]}")


# ---------------------------------------------------------------------------
# Summary / Reports
# ---------------------------------------------------------------------------

def show_summary():
    """Generate a summary report from all CSV files."""
    # --- Students count ---
    _, student_rows = read_csv(STUDENTS_CSV)
    total_students = len(student_rows)

    # --- Attendance summary ---
    _, att_rows = read_csv(ATTENDANCE_CSV)
    present_count = sum(1 for r in att_rows if len(r) >= 3 and r[2] == "P")
    absent_count = sum(1 for r in att_rows if len(r) >= 3 and r[2] == "A")

    # --- Grades summary ---
    _, grade_rows = read_csv(GRADES_CSV)
    total_grades = len(grade_rows)

    print("\n" + "=" * 45)
    print("         SUMMARY REPORT")
    print("=" * 45)
    print(f"Total Students Registered : {total_students}")
    print(f"Attendance Records        : {len(att_rows)}")
    print(f"  - Present               : {present_count}")
    print(f"  - Absent                : {absent_count}")
    print(f"Grades Recorded           : {total_grades}")
    print("=" * 45)


# ---------------------------------------------------------------------------
# Menu & Main Loop
# ---------------------------------------------------------------------------

def display_menu():
    """Show the menu and return the user's choice."""
    print("\n" + "=" * 40)
    print("   Student Record Manager (CSV)")
    print("=" * 40)
    print("1. Add Student")
    print("2. View Students")
    print("3. Mark Attendance")
    print("4. View Attendance")
    print("5. Add Grade")
    print("6. View Grades")
    print("7. Show Summary")
    print("8. Exit")
    return input("Enter your choice: ").strip()


def main():
    """Run the Student Record Manager CLI."""
    ensure_data_dir()

    # Create CSV headers if files don't exist
    for filepath in [STUDENTS_CSV, ATTENDANCE_CSV, GRADES_CSV]:
        if not os.path.exists(filepath):
            append_csv(filepath, [])  # triggers header creation

    while True:
        choice = display_menu()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            mark_attendance()
        elif choice == "4":
            view_attendance()
        elif choice == "5":
            add_grade()
        elif choice == "6":
            view_grades()
        elif choice == "7":
            show_summary()
        elif choice == "8":
            print("Exiting Student Record Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
