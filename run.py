import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('witches_pantry')

def read_logins():
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
    ask_username = str(input('Username: '))
    ask_password = str(input('Password: '))   
    
    logged_in = False
    
    for line in logins:
        if line[0] == ask_username and logged_in == False:
            if line[1] == ask_password:
                logged_in = True
                
    if  logged_in == True:
        print('Logged in successfully')
        main()
    else:
        print('Username / Password is incorrect')
        login()          

def main():
    print(' Welcome To Your Pantry')
    
login()

                                                                                             
                                                                                             