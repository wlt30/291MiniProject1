import sys
import time
import sqlite3
import getpass
import os

def createTable(database, dbcursor, table_name, sql_statement):
    if((sql_statement[0:12]).upper() != "CREATE TABLE"):
        exit
    else:
        database_cursor = database.cursor()
        try:
            dbcursor.execute(("drop table if exists " +table_name +";"))
            dbcursor.execute("PRAGMA foreign_keys = ON;")
            dbcursor.execute(sql_statement)
            print("Successfully created table " +table_name +" in the database")
        except:
            print("Something went wrong with the format of your command, please try again.")
    database.commit()


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
        print('EXITING\nThank you for using this App')
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
            print("Invalid entry, please try again")
            time.sleep(1)
            login_option = int(login_option)
            os.system('cls')

    return login_option

def login(dbcursor):
    print("LOGIN")
    email = input("Email address: ")
    if(email.upper() == "EXIT"):
        exitApp()
    password = getpass.getpass("Password: ")
    # need to verify with Members table from dbcursor
    print("login successful")
    time.sleep(2)
    os.system('cls')

def register(dbcursor):
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
    time.sleep(2)
    os.system('cls')
    
def offerRide(dbcursor):
    print("You selected Offer a Ride")
    
    
def searchForRide(dbcursor):
    print("You selected Search for a Ride")
    
    
def bookMemberOrCancelBooking(dbcursor):
    print("You selected Book Member or Cancel Booking")
    
    
def postRideRequest(dbcursor):
    print("You selected Post Ride Request")
    
    
def searchAndDeleteRequest(dbcursor):
    print("You selected Search and Delete Ride Request")

def mainMenu(dbcursor):
    exiting = False
    while not exiting:
        user_option = input("What would you like to do?\n1.Offer a Ride\n2.Search for Rides\n3.Book Members or Cancel Bookings\n4.Post Ride Request\n5.Search and Delete Ride Request\nAt any point, type EXIT to end your session\n")
        if(user_option == "1"):
            offerRide(dbcursor)
        elif(user_option == "2"):
            searchForRide(dbcursor)
        elif(user_option == "3"):
            bookMemberOrCancelBooking(dbcursor)
        elif(user_option == "4"):
            postRideRequest(dbcursor)
        elif(user_option == "5"):
            searchAndDeleteRequest(dbcursor)
        elif(user_option.upper() == "EXIT"):
            exiting = True
        else:
            print("Not a valid option, please try again")
    time.sleep(1)
    os.system('cls')


def main():
    exiting = False
    database = sqlite3.connect("myDatabase.db")
    dbcursor = database.cursor()

    login_option = entry()
    if(login_option == 1):
        login(dbcursor)
    else:
        register(dbcursor)

    mainMenu(dbcursor)
    
    if exiting:
        database.commit()
        database.close()
        exitApp()
main()
