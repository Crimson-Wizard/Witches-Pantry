import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
from pprint import pprint
import os
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('witches_pantry')
ask_username = None
item_date = None
today = datetime.today()
today_formatted = today.strftime('%d/%m/%Y')


def heading():
    print(r'''
░█░█░▀█▀░▀█▀░█▀▀░█░█░█▀▀░█▀▀░░█▀█░█▀█░█▀█░▀█▀░█▀▄░█░█
░█▄█░░█░░░█░░█░░░█▀█░█▀▀░▀▀█░░█▀▀░█▀█░█░█░░█░░█▀▄░░█░
░▀░▀░▀▀▀░░▀░░▀▀▀░▀░▀░▀▀▀░▀▀▀░░▀░░░▀░▀░▀░▀░░▀░░▀░▀░░▀░
    ''')


def clearConsole():
    command = "clear"
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)


def read_logins():
    """
    funtion to read user name and password and split into two fields
    """
    try:
        users_worksheet = SHEET.worksheet('users')
        records = users_worksheet.get_all_records()
        new_contents = [[record['Username'], record['Password']]
                        for record in records]
        return new_contents
    except Exception as e:
        print(f"Failed to read logins from sheet: {e}")
        return []


logins = read_logins()


def login():
    """
    funtion to enter user name and password to login
    """
    global ask_username
    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        ask_username = input('Username:\n')
        ask_password = input('Password:\n')

        for line in logins:
            if line[0] == ask_username and line[1] == ask_password:
                print(f'Logged in successfully, welcome to your pantry {
                      ask_username}')
                return True

        print('Username / Password is incorrect')
        attempts += 1

    print("Login failed. Please contact admin.")
    return False


def add_item():
    """
    function to add item to list.
    then seperate input into two values
    then convert the seconf input into date format
    """
    global item_date

    while True:
        print("Please enter item to pantry")
        print("Enter Item name and date in non US format dd/mm/yyyy")
        print("Example: Cheese,20/04/2023 no space after comma\n")

        item_str = input("Enter:\n")
        item_date = item_str.split(",")

        if validate_data(item_date):
            date_str = item_date[1]
            date = datetime.strptime(date_str, "%d/%m/%Y")
            formatted_date = date.strftime('%d/%m/%Y')
            item_date[1] = formatted_date
            break

    return item_date

    select_function()


def validate_data(values):
    """
    function to validate input values item & date.
    check if date format is correct.
    """
    today = datetime.today().date()

    try:
        if len(values) != 2:
            raise ValueError("Item and Use By Date required")

        # Parse date and strip whitespace
        item_date = datetime.strptime(values[1].strip(), "%d/%m/%Y").date()
        if item_date < today:
            raise ValueError("Item date cannot be in the past.")

        print(f"Validating date: {values[1]}")
        datetime.strptime(values[1], "%d/%m/%Y")
        print('Item added')

    except ValueError as e:
        print(f"Invalid data: {e}. Please try again.")
        return False

    return True

    select_function()


def add_item_to_pantry(item_date):
    """
    funtion to add item to spreadsheet
    both item and date to bottom of spread sheet
    """
    print("updating pantry....\n")
    pantry_worksheet = SHEET.worksheet(ask_username)
    pantry_worksheet.append_row(item_date, value_input_option='USER_ENTERED')
    select_function()


def expired_items():
    """
    function to see display item past use by date
    """
    worksheet = SHEET.worksheet(f'{ask_username}')
    records = worksheet.get_all_values()
    headers = records[0]
    data = records[1:]

    try:
        date_idx = headers.index('Use by date')
    except ValueError:
        print("Error: 'Date' column not found.")
        return

    today = datetime.today().strftime('%d/%m/%Y')
    upcoming_items = []

    for row in data:
        item_date = row[date_idx].strip()
        if item_date <= today:
            upcoming_items.append(row)

    if upcoming_items:
        print("\nOut of date items:\n")
        for item in upcoming_items:
            pprint(item)
    else:
        print("No items out of date.")


def items_expiring_today():
    """
    function to see items today
    """
    worksheet = SHEET.worksheet(f'{ask_username}')
    records = worksheet.get_all_values()
    headers = records[0]
    data = records[1:]

    try:
        date_idx = headers.index('Use by date')
    except ValueError:
        print("Error: 'Date' column not found.")
        return

    today = datetime.today().strftime('%d/%m/%Y')
    upcoming_items = []

    for row in data:
        item_date = row[date_idx].strip()
        if item_date == today:
            upcoming_items.append(row)

    if upcoming_items:
        print("Items expiring today:")
        for item in upcoming_items:
            pprint(item)
    else:
        print("No items expiring today.")

    select_function()


def one_week():
    """
    function to see items 1 week
    """
    one_week = today + timedelta(days=7)
    worksheet = SHEET.worksheet(f'{ask_username}')
    records = worksheet.get_all_values()
    headers = records[0]
    data = records[1:]

    date_idx = headers.index('Date') if 'Date' in headers else 1

    upcoming_items = []
    for row in data:
        try:
            item_date = datetime.strptime(row[date_idx], '%d/%m/%Y')
            if today <= item_date <= one_week:
                upcoming_items.append(row)
        except ValueError:
            continue

    if upcoming_items:
        print("Items expiring within the next week:")
        for item in upcoming_items:
            pprint(item)
    else:
        print("No items expiring within the next week.")

    select_function()


def two_weeks():
    """
    function to see items 2 week
    """
    two_week = today + timedelta(days=14)
    worksheet = SHEET.worksheet(f'{ask_username}')
    records = worksheet.get_all_values()
    headers = records[0]
    data = records[1:]

    date_idx = headers.index('Date') if 'Date' in headers else 1

    upcoming_items = []
    for row in data:
        try:
            item_date = datetime.strptime(row[date_idx], '%d/%m/%Y')
            if today <= item_date <= two_week:
                upcoming_items.append(row)
        except ValueError:
            continue

    if upcoming_items:
        print("Items expiring within the next two weeks:")
        for item in upcoming_items:
            pprint(item)
    else:
        print("No items expiring within the next two week.")

    select_function()


def three_weeks():
    """
    function to see items 2 week
    """
    three_week = today + timedelta(days=21)
    worksheet = SHEET.worksheet(f'{ask_username}')
    records = worksheet.get_all_values()
    headers = records[0]
    data = records[1:]

    date_idx = headers.index('Date') if 'Date' in headers else 1

    upcoming_items = []
    for row in data:
        try:
            item_date = datetime.strptime(row[date_idx], '%d/%m/%Y')
            if today <= item_date <= three_week:
                upcoming_items.append(row)
        except ValueError:
            continue

    if upcoming_items:
        print("Items expiring within the next three weeks:")
        for item in upcoming_items:
            pprint(item)
    else:
        print("No items expiring within the next three weeks.")

    select_function()


def delete_item():
    """
    funtion to delete item from spreadsheet
    """
    expired_items()
    print("\nInput item name to delete:\n")
    worksheet = SHEET.worksheet(ask_username)
    records = worksheet.get_all_values()
    headers = records[0]
    data = records[1:]

    try:
        item_idx = headers.index('Item')
    except ValueError:
        print("The 'Item' column was not found in the worksheet.")
        return

    remove_item = input('Item to delete:\n')

    found = False
    for idx, row in enumerate(data, start=2):
        if row[item_idx] == remove_item:
            worksheet.delete_rows(idx)
            print(f"Item '{remove_item}' deleted successfully.")
            found = True
            break

    if not found:
        print(f"Item '{remove_item}' not found in the worksheet.")

    select_function()


def select_function():
    """
    Function to give user the option to select what function to use
    and to loop until user decides to exit.
    """
    while True:
        print("\nPlease select an option:")
        print("1. Add an Item")
        print("2. Items Expiring today")
        print("3. Show Items Expiring in One Week")
        print("4. Show Items Expiring in Two Weeks")
        print("5. Show Items Expiring in Three Weeks")
        print("6. Delete an Item")
        print("7. Log Out")

        choice = input("Enter your choice (1-7):\n")

        if choice == '7':
            print("Logging out...")
            main()
            break

        if choice in ('1', '2', '3', '4', '5', '6'):
            try:
                functions = {
                    '1': add_item,
                    '2': items_expiring_today,
                    '3': one_week,
                    '4': two_weeks,
                    '5': three_weeks,
                    '6': delete_item
                }
                functions[choice]()
            except KeyError:
                print("Invalid choice. Please try again.")
        else:
            print("Invalid choice. Please try again.")


def main():
    """
    Main function to handle the initial login
    and transfer to the selection menu.
    """
    clearConsole()
    if login():
        clearConsole()
        heading()
        select_function()
    else:
        print("Failed to login. Exiting the program.")


if __name__ == "__main__":
    main()
