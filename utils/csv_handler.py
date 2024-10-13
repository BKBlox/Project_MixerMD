import csv
import os

CSV_FILE_PATH = 'data/users.csv'

def write_to_csv(data):
    """Append a new row to the CSV file."""
    file_exists = os.path.isfile(CSV_FILE_PATH)

    with open(CSV_FILE_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(data.keys())  # Write headers if file doesn't exist
        writer.writerow(data.values())

def read_from_csv():
    """Read all rows from the CSV file and return them as a list of dictionaries."""
    if not os.path.isfile(CSV_FILE_PATH):
        return []

    with open(CSV_FILE_PATH, mode='r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def update_row_in_csv(user_id, new_data):
    """Update an existing row in the CSV file based on user ID."""
    rows = read_from_csv()
    updated = False

    for row in rows:
        if row['user_id'] == user_id:
            row.update(new_data)  # Update the row with new data
            updated = True
            break

    if updated:
        with open(CSV_FILE_PATH, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        return True
    return False