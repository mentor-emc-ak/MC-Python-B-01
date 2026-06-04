from datetime import datetime


STUDENTS = [
	"Akhil",
	"Divya",
	"Karthik",
	"Meena",
	"Surya",
]


attendance_records = {}


def get_attendance_date():
	"""Ask the user for a date in YYYY-MM-DD format."""
	while True:
		date_text = input("Enter attendance date (YYYY-MM-DD): ").strip()

		try:
			datetime.strptime(date_text, "%Y-%m-%d")
			return date_text
		except ValueError:
			print("Invalid date format. Please use YYYY-MM-DD.")


def get_attendance_status(student_name):
	"""Return Present or Absent based on the user's choice."""
	while True:
		choice = input(f"Is {student_name} present? (P/A): ").strip().lower()

		if choice == "p":
			return "Present"
		if choice == "a":
			return "Absent"

		print("Invalid choice. Enter P for Present or A for Absent.")


def mark_attendance():
	"""Collect attendance for every student on a selected date."""
	attendance_date = get_attendance_date()
	daily_attendance = {}

	print(f"\nMarking attendance for {attendance_date}")
	print("-" * 35)

	for student in STUDENTS:
		daily_attendance[student] = get_attendance_status(student)

	attendance_records[attendance_date] = daily_attendance
	print(f"Attendance saved for {attendance_date}.")


def show_students():
	"""Display the student list."""
	print("\nStudent List")
	print("-" * 20)

	for index, student in enumerate(STUDENTS, start=1):
		print(f"{index}. {student}")


def view_attendance():
	"""Display attendance records grouped by date."""
	if not attendance_records:
		print("No attendance has been recorded yet.")
		return

	print("\nAttendance Records")
	print("-" * 25)

	for attendance_date in sorted(attendance_records):
		print(f"\nDate: {attendance_date}")
		for student, status in attendance_records[attendance_date].items():
			print(f"{student}: {status}")


def show_summary():
	"""Display summary counts by date and by student."""
	if not attendance_records:
		print("No attendance has been recorded yet.")
		return

	print("\nSummary by Date")
	print("-" * 25)

	total_present = 0
	total_absent = 0
	student_summary = {student: {"Present": 0, "Absent": 0} for student in STUDENTS}

	for attendance_date in sorted(attendance_records):
		daily_attendance = attendance_records[attendance_date]
		present_count = sum(1 for status in daily_attendance.values() if status == "Present")
		absent_count = sum(1 for status in daily_attendance.values() if status == "Absent")

		total_present += present_count
		total_absent += absent_count

		for student, status in daily_attendance.items():
			student_summary[student][status] += 1

		print(f"{attendance_date} -> Present: {present_count}, Absent: {absent_count}")

	print("\nOverall Counts")
	print("-" * 20)
	print(f"Total Present: {total_present}")
	print(f"Total Absent: {total_absent}")

	print("\nSummary by Student")
	print("-" * 25)
	for student in STUDENTS:
		print(
			f"{student} -> Present: {student_summary[student]['Present']}, "
			f"Absent: {student_summary[student]['Absent']}"
		)


def display_menu():
	"""Show the menu and return the selected option."""
	print("\nStudent Attendance Tracker")
	print("1. Show student list")
	print("2. Mark attendance")
	print("3. View attendance")
	print("4. Show summary")
	print("5. Exit")
	return input("Enter your choice: ").strip()


def main():
	"""Run the attendance tracker terminal program."""
	while True:
		choice = display_menu()

		if choice == "1":
			show_students()
		elif choice == "2":
			mark_attendance()
		elif choice == "3":
			view_attendance()
		elif choice == "4":
			show_summary()
		elif choice == "5":
			print("Exiting attendance tracker.")
			break
		else:
			print("Invalid choice. Please enter a number from 1 to 5.")


main()
