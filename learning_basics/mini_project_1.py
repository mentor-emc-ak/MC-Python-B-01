import json
import os
from datetime import datetime


# Save the JSON file in the same folder as this Python script.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "attendance_data.json")


def load_data():
	"""Load students and attendance data from the JSON file."""
	default_data = {
		"students": [],
		"attendance": {}
	}

	# Create the file automatically if it does not exist yet.
	if not os.path.exists(DATA_FILE):
		save_data(default_data)
		return default_data

	try:
		with open(DATA_FILE, "r", encoding="utf-8") as file:
			data = json.load(file)

		# Make sure the loaded data has the expected structure.
		if "students" not in data or "attendance" not in data:
			print("Data file format was incomplete. Starting with empty data.")
			save_data(default_data)
			return default_data

		if not isinstance(data["students"], list) or not isinstance(data["attendance"], dict):
			print("Data file format was invalid. Starting with empty data.")
			save_data(default_data)
			return default_data

		return data
	except (json.JSONDecodeError, OSError):
		# If the file cannot be read, start again with empty data.
		print("Could not read the data file. Starting with empty data.")
		save_data(default_data)
		return default_data


def save_data(data):
	"""Save students and attendance data to the JSON file."""
	with open(DATA_FILE, "w", encoding="utf-8") as file:
		json.dump(data, file, indent=4)


def add_student(data):
	"""Ask the user for a student name and add it if it is not a duplicate."""
	name = input("Enter the student's name: ").strip()

	# Reject empty input so blank names are not saved.
	if not name:
		print("Student name cannot be empty.")
		return

	# Check for duplicates without caring about uppercase/lowercase differences.
	for student in data["students"]:
		if student.lower() == name.lower():
			print("This student already exists.")
			return

	data["students"].append(name)
	data["students"].sort()
	print(f"Student '{name}' added successfully.")


def mark_attendance(data):
	"""Record today's attendance for a selected student."""
	if not data["students"]:
		print("No students found. Add a student first.")
		return

	print("\n===== STUDENT LIST =====")
	for index, student in enumerate(data["students"], start=1):
		print(f"{index}. {student}")

	choice = input("Select a student by number: ").strip()

	# Validate that the user entered a number from the list.
	if not choice.isdigit():
		print("Please enter a valid number.")
		return

	student_index = int(choice) - 1
	if student_index < 0 or student_index >= len(data["students"]):
		print("Selected student number is out of range.")
		return

	selected_student = data["students"][student_index]
	today = datetime.now().strftime("%Y-%m-%d")

	# Create a new date section if attendance has not been marked for today yet.
	if today not in data["attendance"]:
		data["attendance"][today] = {}

	# Prevent multiple attendance entries for the same student on the same date.
	if selected_student in data["attendance"][today]:
		print(f"Attendance for {selected_student} has already been recorded today.")
		return

	print("\nChoose attendance status:")
	print("1. Present")
	print("2. Absent")
	status_choice = input("Enter your choice: ").strip()

	if status_choice == "1":
		status = "Present"
	elif status_choice == "2":
		status = "Absent"
	else:
		print("Invalid status choice.")
		return

	data["attendance"][today][selected_student] = status
	print(f"Attendance marked: {selected_student} - {status} on {today}.")


def view_attendance(data):
	"""Display all attendance records in a neat table format."""
	if not data["attendance"]:
		print("No attendance records found.")
		return

	print("\n===== ATTENDANCE RECORDS =====")
	print(f"{'Student Name':<20} {'Date':<12} {'Status':<10}")
	print("-" * 44)

	# Show records in date order, and student names in alphabetical order.
	for record_date in sorted(data["attendance"]):
		daily_records = data["attendance"][record_date]
		for student in sorted(daily_records):
			status = daily_records[student]
			print(f"{student:<20} {record_date:<12} {status:<10}")


def display_menu():
	"""Show the menu and return the user's choice."""
	print("\n===== ATTENDANCE TRACKER =====")
	print("1. Add Student")
	print("2. Mark Attendance")
	print("3. View Attendance")
	print("4. Save Data")
	print("5. Exit")
	return input("Enter your choice: ").strip()


def main():
	"""Run the main program loop for the Attendance Tracker."""
	data = load_data()

	while True:
		choice = display_menu()

		if choice == "1":
			add_student(data)
		elif choice == "2":
			mark_attendance(data)
		elif choice == "3":
			view_attendance(data)
		elif choice == "4":
			save_data(data)
			print("Data saved successfully.")
		elif choice == "5":
			# Save once more before exiting so the latest changes are not lost.
			save_data(data)
			print("Data saved. Exiting Attendance Tracker.")
			break
		else:
			print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
	main()
