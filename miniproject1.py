import sys
import time
import sqlite3
import getpass
import os

def insertValues(database, dbcursor, table_name, sql_statement):
    if((sql_statement[0:11]).upper() != "INSERT INTO"):
        exit
    else:
        try:
            dbcursor.execute(sql_statement)
            print("Successfully inserted values into " +table_name)
        except:
            print("Something went wrong with the format of your command, please try again.")
    database.commit()

def exitApp():
        os.system("cls")
        print('EXITING\nThank you for using this Ride Finder')
        time.sleep(2)
        sys.exit()

def entry():
    #controlled login screen, only allows for Login and Register options
    login_option = 0
    while(login_option<1 or login_option>2):
        login_option = (input("Select 1 to login as an existing user, or press 2 to register\nAt any point, type EXIT to end your session\n"))
        if login_option.upper() == "EXIT":
            exitApp()
        if not (login_option[0].isdigit()):
            print("Invalid entry, please try again")
            time.sleep(1)
            login_option = 0
            os.system('cls')
        else:
            login_option = int(login_option)
            os.system('cls')
    return login_option

def login(dbcursor):
    os.system('cls')
    validEmail = False
    validPass = False
    print("LOGIN\nAt any point, type BACK to go back to Login Options")
    while not validEmail:
        email = input("Email address: ")
        if(email.upper() == "EXIT"):
            exitApp()
        if(email.upper() == "BACK"):
            entry()
        dbcursor.execute("SELECT email FROM members")
        emailList = dbcursor.fetchall()
        for item in emailList:
            if item[0] == email:
                validEmail = True
        if not validEmail:
            print("An account with that email does not exist, please try again")
        
    while not validPass:
        password = getpass.getpass("Password: ")
        if(password.upper() == "BACK"):
                entry()
        dbcursor.execute("SELECT pwd FROM members WHERE email = \""+email +"\"")
        correctPass = dbcursor.fetchone()
        if password == correctPass[0]:
            validPass = True
            print("login successful")
        else:
            print("Incorrect password, please try again or type BACK to return")
    
    time.sleep(1)

def register(dbcursor):
    os.system('cls')
    print("REGISTER\nPlease provide the following:")
    email = input("Email address: ")
    if(email.upper() == "EXIT"):
        exitApp()
    name = input("Name: ")
    if name.upper() == "EXIT":
        exitApp()
    phone = input("Phone: ")
    if phone.upper() == "EXIT":
        exitApp()
    password = getpass.getpass("Password: ")
    # ensure unique password against existing Members
    print("Registration successful")
    time.sleep(1)
    os.system('cls')
    
def offerRide(dbcursor):
    os.system('cls')
    print("You selected Offer a Ride")
    dbcursor.execute("SELECT * FROM members")
    members = dbcursor.fetchall()
    for member in members:
        print(member)
    
def searchForRide(dbcursor):
    os.system('cls')
    print("You selected Search for a Ride")
    
    
def bookMemberOrCancelBooking(dbcursor):
    os.system('cls')
    print("You selected Book Member or Cancel Booking")
    
    
def postRideRequest(dbcursor):
    os.system('cls')
    print("You selected Post Ride Request")
    
    
def searchAndDeleteRequest(dbcursor):
    os.system('cls')
    print("You selected Search and Delete Ride Request")

def mainMenu(dbcursor):
    os.system('cls')
    exiting = False
    while not exiting:
        user_option = input("What would you like to do?\n1.Offer a Ride\n2.Search for Rides\n3.Book Members or Cancel Bookings\n4.Post Ride Request\n5.Search and Delete Ride Request\nAt any point, type EXIT to end your session\n")
        if(user_option == "1"):
            time.sleep(1)
            os.system('cls')
            offerRide(dbcursor)
        elif(user_option == "2"):
            time.sleep(1)
            os.system('cls')
            searchForRide(dbcursor)
        elif(user_option == "3"):
            time.sleep(1)
            os.system('cls')
            bookMemberOrCancelBooking(dbcursor)
        elif(user_option == "4"):
            time.sleep(1)
            os.system('cls')
            postRideRequest(dbcursor)
        elif(user_option == "5"):
            time.sleep(1)
            os.system('cls')
            searchAndDeleteRequest(dbcursor)
        elif(user_option.upper() == "EXIT"):
            exitApp()
        else:
            print("Not a valid option, please try again")

def main():
    exiting = False
    database = sqlite3.connect("testDatabase.db")
    dbcursor = database.cursor()
    print("Welcome to Ride Finder")
    time.sleep(1)
    login_option = entry()
    if(login_option == 1):
        login(dbcursor)
    else:
        register(dbcursor)
    mainMenu(dbcursor)
    # main activity, will continue to run unless explicitly exited    
    if exiting:
        database.commit()
        database.close()
        exitApp()
main()
