import gspread
from google.oauth2.service_account import Credentials 
from datetime import datetime

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
    """
    funtion to enter user name and password to login
    """

    ask_username = str(input('Username: '))
    ask_password = str(input('Password: '))   
    
    logged_in = False
    
    for line in logins:
        if line[0] == ask_username and logged_in == False:
            if line[1] == ask_password:
                logged_in = True
                break
                
    if  logged_in == True:
        print('Logged in successfully, welcome to your pantry')
        main()
    else:
        print('Username / Password is incorrect')
        login()  


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

        item_str = input("Enter:")
        

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
   



"""
function to see items 1 week, 2 weeks, ,3 weeks, 1 month 
"""

def main():
    """
    Run all main funtions
    """  
login()
item_date = add_item()
add_item_to_pantry(item_date) 
                                                                                                                                                                    