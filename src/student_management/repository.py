"""CSV-based data persistence layer for Student Management System."""

import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class CSVRepository:
       """Handles reading/writing data to CSV files.

     Provides methods for CRUD operations on CSV data.
     All file paths are validated and directories auto-created.
      """

    def __init__(self, filepath: str | Path):
        self.filepath = Path(filepath).resolve()
         if not self.filepath.parent.exists():
             logger.info(f"Creating directory: {self.filepath.parent}")
            self.filepath.parent.mkdir(parents=True, exist_ok=True)

    def ensure_file(self, headers: list[str]) -> None:
        """Create the CSV file with headers if it doesn't exist.

     Args:
         headers: Column names to write as the header row.
      """
     if not self.filepath.exists():
        with open(self.filepath, "w", newline="") as f:
            writer = csv.writer(f)
             writer.writerow(headers)
          logger.info(f"Created {self.filepath} with headers: {headers}")

    def read_all(self) -> list[list[str]]:
         """Read all data rows from the CSV file, skipping the header.

     Returns:
         List of row lists (each row is a list of strings).
      """
     if not self.filepath.exists():
        return []
     with open(self.filepath, "r", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header
         return [row for row in reader]

    def append_row(self, row: list[str]) -> None:
       """Append a single row to the CSV file.

     Args:
         row: List of values to write as a new row.
      """
    with open(self.filepath, "a", newline="") as f:
        writer = csv.writer(f)
         writer.writerow(row)
      logger.debug(f"Appended row to {self.filepath}")

    def delete_all(self) -> None:
       """Clear all data rows while keeping the header intact.

     Creates a fresh file with only the original headers if none exist,
     or overwrites with just the header row.
     Raises:
         IOError: If unable to write to the file.
      """
    try:
        # Determine header from existing file or create new one
        if self.filepath.exists():
            with open(self.filepath, "r", newline="") as f:
                reader = csv.reader(f)
                 headers = next(reader, [])
           else:
             headers = []

         # Overwrite with only header row (clears all data)
        with open(self.filepath, "w", newline="") as f:
            writer = csv.writer(f)
            if headers:
                writer.writerow(headers)
          logger.info(f"Cleared all rows from {self.filepath}")
    except IOError as e:
        logger.error(f"Failed to clear {self.filepath}: {e}")
         raise

    def read_header(self) -> list[str]:
       """Read the header row from the CSV file.

     Returns:
         List of column names, empty list if file doesn't exist or is empty.
      """
    if not self.filepath.exists():
        return []
     with open(self.filepath, "r", newline="") as f:
        reader = csv.reader(f)
         return next(reader, [])

    def write_all(self, headers: list[str], rows: list[list[str]]) -> None:
       """Overwrite the entire file with new data.

     Args:
         headers: Column names for the header row.
         rows: Data rows to write.

     Raises:
        IOError: If unable to write to the file.
      """
    try:
        with open(self.filepath, "w", newline="") as f:
             writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
         logger.debug(f"Wrote {len(rows)} rows to {self.filepath}")
    except IOError as e:
        logger.error(f"Failed to write to {self.filepath}: {e}")
         raise

    def find_by(self, column_index: int, value: str) -> list[list[str]]:
       """Find all rows where column at column_index matches value.

     Args:
         column_index: Zero-based column index to search.
         value: String value to match exactly.

     Returns:
         List of matching row lists.
      """
    all_rows = self.read_all()
     return [row for row in all_rows if len(row) > column_index and row[column_index] == value]

    def exists(self, column_index: int, value: str) -> bool:
       """Check if any row has the given value in the specified column.

     Args:
         column_index: Zero-based column index to search.
         value: String value to match exactly.

     Returns:
         True if at least one matching row exists.
      """
    return len(self.find_by(column_index, value)) > 0

    def update_row(self, key_column_index: int, key_value: str, new_row: list[str]) -> bool:
       """Update a row in place based on a key column match.

     Args:
         key_column_index: Column index used as the lookup key.
         key_value: Value to match in the key column.
         new_row: Replacement row data.

     Returns:
         True if row was found and updated, False if key not found.
      """
    all_rows = self.read_all()
     headers = self.read_header() or [f"col_{i}" for i in range(max(len(r) for r in all_rows), default=0)]

    updated = False
    new_rows = []
    for row in all_rows:
         if len(row) > key_column_index and row[key_column_index] == key_value:
             new_rows.append(new_row)
             updated = True
           logger.info(f"Updated row with key {key_value} in {self.filepath}")
       else:
          new_rows.append(row)

     if updated:
         self.write_all(headers, new_rows)
    return updated
