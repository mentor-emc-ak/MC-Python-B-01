"""CSV-based data persistence layer for Student Management System."""

import csv
import os


class CSVRepository:
    """Handles reading/writing data to CSV files."""

    def __init__(self, filepath: str):
        self.filepath = filepath

    def ensure_file(self, headers: list[str]) -> None:
        """Create the CSV file with headers if it doesn't exist."""
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath) or ".", exist_ok=True)
            with open(self.filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)

    def read_all(self) -> list[list[str]]:
        """Read all rows from the CSV file. Returns list of row lists."""
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)   # Skip header
            return [row for row in reader]

    def append_row(self, row: list[str]) -> None:
        """Append a single row to the CSV file."""
        with open(self.filepath, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def delete_all(self) -> None:
        """Clear all data rows (keep headers)."""
        rows = self.read_all()
        if not rows:
            return
        with open(self.filepath, "w", newline="") as f:
            writer = csv.writer(f)
            # Re-read header
            with open(self.filepath, "r", newline="") as rf:
                header = next(rf, [])
                writer.writerow(header)
                writer.writerows(rows)   # Write back (this is a no-op if rows empty)

    def find_by(self, column_index: int, value: str) -> list[list[str]]:
        """Find rows where column at column_index equals value."""
        all_rows = self.read_all()
        return [row for row in all_rows if len(row) > column_index and row[column_index] == value]

    def exists(self, column_index: int, value: str) -> bool:
        """Check if any row has the given value in the specified column."""
        return len(self.find_by(column_index, value)) > 0
