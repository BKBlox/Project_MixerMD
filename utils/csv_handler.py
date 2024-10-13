import csv
import os

CSV_FILE_PATH = 'data/users.csv'

def write_to_csv(data): # will need to somehow return unique user id to user website
    """Append a new row to the CSV file."""
    current_dir = os.path.dirname(__file__)  # Directory where csv_handler.py is located
    FILE_PATH = os.path.join(current_dir, '../data/users.csv') # FINAL, DO NOT CHANGE UNLESS DATA PATH CHANGES

    with open(FILE_PATH, 'r') as file:
        user_uuid = sum(1 for line in file) + 1
    with open(FILE_PATH, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "ans1", "ans2", "ans3", "ans4", "ans5",
                                                  "ans6", "ans7", "ans8", "ans9", "ans10", "uuid"])
        writer.writerow({"name":data.get("name"), "ans1":data.get("ans1"), "ans2":data.get("ans2"), "ans3":data.get("ans3"),
                         "ans4":data.get("ans4"), "ans5":data.get("ans5"), "ans6":data.get("ans6"), "ans7":data.get("ans7"),
                         "ans8":data.get("ans8"), "ans9":data.get("ans9"), "ans10":data.get("ans10"), "uuid":user_uuid})
    return user_uuid

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