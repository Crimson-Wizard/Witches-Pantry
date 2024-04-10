import gspread
from google.oauth2.service_account import Credentials 
from datetime import datetime, timedelta 

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('witches_pantry')
ask_username =  None 
today = datetime.today()
today_formatted = today.strftime('%d/%m/%Y')

def read_logins():
    """
    funtion to read user name and password and split into two fields
    """
    with open('logins.txt', 'r') as f:
        contents = f.readlines()
        
        new_contents = []
        
        for line in contents:
            fields = line.split(',')
            fields[1] = fields[1].rstrip()
            new_contents.append(fields)
        
        return(new_contents)
logins = read_logins()       
                                                                                                 
def login():
    global ask_username
    max_attempts = 3  # Limit the number of login attempts to prevent infinite loops
    attempts = 0
    """
    funtion to enter user name and password to login
    """
    while attempts < max_attempts:
        ask_username = input('Username:\n')
        ask_password = input('Password:\n')   
        
        for line in logins:
            if line[0] == ask_username and line[1] == ask_password:
                print(f'Logged in successfully, welcome to your pantry {ask_username}')
                return True  # Return True to indicate a successful login
        
        print('Username / Password is incorrect')
        attempts += 1  # Increment the attempt counter
    
    print("Login failed. Please contact admin.")
    return False 



def add_item():
    """
    function to add item to list. 
    then seperate input into two values
    then convert the seconf input into date format
    """
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

def validate_data(values):
    """
    function to validate input values  1(0) item 2(1) date. check if date format is correct.
    """

    try:
        if len(values) != 2:
            raise ValueError("Item and Use By Date required")

        print(f"Validating date: {values[1]}")
        datetime.strptime(values[1], "%d/%m/%Y")

    except ValueError as e:
        print(f"Invalid data: {e}. Please try again.")   
        return False  

    return True

def add_item_to_pantry(item_date):
    """
    funtion to add item to spreadsheet both item and date to bottom of spread sheet
    """
    print("updating pantry....\n")
    pantry_worksheet = SHEET.worksheet(ask_username)
    pantry_worksheet.append_row(item_date, value_input_option='USER_ENTERED')
   
def one_week():
    """
    function to see items 1 week
    """
    one_week = today + timedelta(days=7)
    one_week_formated = one_week.strftime('%d/%m/%Y')
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

def two_weeks():
    """
    function to see items 2 week
    """    
    two_week = today + timedelta(days=14)
    two_week_formated = two_week.strftime('%d/%m/%Y')
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
        print("No items expiring within the next week.")
 
def three_weeks():
    """
    function to see items 2 week
    """
    three_week = today + timedelta(days=21)
    three_week_formated = three_week.strftime('%d/%m/%Y')
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
        print("No items expiring within the next week.")

def delete_item():
    """
    funtion to delete item from spreadsheet 
    """
    print("Input item name to delete:\n")
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

def select_function():
    """
    Function to give user option to select what function to use
    """

    functions = {
    '1': add_item,
    '2': one_week,
    '3': two_weeks,
    '4': three_weeks,
    '5': delete_item,  
    }

    print("Please select an option:")
    print("1. Add an Item")
    print("2. Show Items Expiring in One Week")
    print("3. Show Items Expiring in Two Weeks")
    print("4. Show Items Expiring in Three Weeks")
    print("5. Delete an Item")

    choice = input("Enter your choice 1-5 here:\n")

    if choice in functions:
        functions[choice]()

    else:
        print('Invalid choice. Please try again.')



def main():
    """
    Run all main functions
    """  
    if login():
        select_function()
    else:
        print("Exiting...")

if __name__ == "__main__":
    main()                                                                                                                                      