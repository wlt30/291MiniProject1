import sys
import time
import sqlite3
import getpass
import os
import datetime
import platform
import offerRide
import searchRides
import searchRequest
import Bookings
import postRideRequest

if((platform.system()) == "Windows"):
    cls = 'cls'
elif((platform.system()) == "Linux"):
    cls = 'clear'
elif((platform.system()) == "Darwin"):
    cls = 'clear'

def exitApp(database):
        os.system(cls)
        print('EXITING...\nThank you for using Ride Finder')
        time.sleep(2)
        database.commit()
        database.close()
        database.close()
        sys.exit()

def entry(database):
    #controlled login screen, only allows for Login and Register options
    login_option = 0
    while(login_option<1 or login_option>2):
        login_option = (input("Select 1 to login as an existing user, or press 2 to register\nAt any point, type EXIT to end your session\n"))
        if login_option.upper() == "EXIT":
            exitApp(database)
        if not (login_option[0].isdigit()):
            print("Invalid entry, please try again")
            time.sleep(1)
            login_option = 0
            os.system(cls)
        else:
            login_option = int(login_option)
            os.system(cls)
    return login_option

def login(database, dbcursor):
    os.system(cls)
    validEmail = False
    validPass = False
    print("LOGIN\nAt any point, type BACK to go back")
    while not validEmail:
        # receives user input for email and checks the validity of this email address in the database
        email = input("Email address: ")
        if(email.upper() == "EXIT"):
            exitApp(database)
        if(email.upper() == "BACK"):
            entry(database)
        dbcursor.execute("SELECT email FROM members WHERE email = \""+email +"\"")
        emailList = dbcursor.fetchall()
        if len(emailList)>0 and email != "email":
            # !=email statement protects against SQL injection
            validEmail = True
        if not validEmail:
            print("An account with that email does not exist, please try again")

    while not validPass:
        # receives hidden user input for password and checks validity of this password for the given email address
        password = getpass.getpass("Password: ")
        if(password.upper() == "BACK"):
                entry()
        dbcursor.execute("SELECT pwd FROM members WHERE email = \""+email +"\"")
        correctPass = dbcursor.fetchone()
        if password == correctPass[0] and email != "email":
            # statements prevent against SQL injection inputs of password or email
            validPass = True
            print("login successful")
        else:
            print("Incorrect password, please try again or type BACK to return")

    return email
    time.sleep(1)

def register(dbcursor):
    os.system(cls)
    print("REGISTER\nPlease provide the following:")
    availableEmail = False
    validName = False
    validPhone = False
    validPwd = False
    while not availableEmail:
        email = input("Email address(max 15 charcters): ")
        if(email.upper() == "EXIT"):
            exitApp()
        if(email.upper() == "BACK"):
            entry()
        if len(email)>15:
            print("Entered email too long, please try again")
            continue
        elif len(email)==0:
            continue
        dbcursor.execute("SELECT email FROM members WHERE email = \""+email +"\"")
        emailList = dbcursor.fetchall()
        if len(emailList)==0:
            availableEmail = True
        if not availableEmail:
            print("An account with that email already exists")

    while not validName:
        name = input("Name (max 20 characters): ")
        if(name.upper() == "EXIT"):
            exitApp()
        if(name.upper() == "BACK"):
            entry()
        if len(name)>20:
            print("Entered name is too long, please try again")
            continue
        elif len(name)==0:
            continue
        else:
            validName = True

    while not validPhone:
        phone = input("Phone (e.g.123-555-1234): ")
        if(phone.upper() == "EXIT"):
            exitApp()
        if(phone.upper() == "BACK"):
            entry()
        if len(phone)>12:
            print("Entered phone number too long, please try again")
            continue
        if len(phone)<12:
            print("Entered phone number too short or incorrect format, please try again\n(e.g.123-555-1234)")
            continue
        elif len(phone)==0:
            continue
        else:
            validPhone = True

    while not validPwd:
        password = getpass.getpass("Password (max 6 characters): ")
        if(password.upper() == "EXIT"):
            exitApp()
        if(password.upper() == "BACK"):
            entry()
        if len(password)>6:
            print("Entered password number too long, please try again")
            continue
        elif len(password)==0:
            continue
        else:
            validPwd = True

    dbcursor.execute("INSERT INTO members VALUES (\""+email+"\",\""+name+"\",\""+phone+"\",\""+password+"\")")
    print("Registration successful")
    return email


def mainMenu(database, dbcursor, member):
    os.system(cls)
    exiting = False
    while not exiting:
        user_option = input("What would you like to do?\n1.Offer a Ride\n2.Search for Rides\n3.Book Members or Cancel Bookings\n4.Post Ride Request\n5.Search and Delete Ride Request\n6.Logout\nAt any point, type EXIT to end your session\n")
        if(user_option == "1"):
            time.sleep(0.5)
            offerRide.offerRide(dbcursor, member)
            database.commit()
        elif(user_option == "2"):
            time.sleep(0.5)
            searchRides.searchForRide(database, dbcursor, member)
            database.commit()
        elif(user_option == "3"):
            time.sleep(0.5)
            Bookings.Bookings(dbcursor, member)
            database.commit()
        elif(user_option == "4"):
            time.sleep(0.5)
            postRideRequest.postRideRequest(dbcursor, member)
            database.commit()
        elif(user_option == "5"):
            time.sleep(0.5)
            searchRequest.searchAndDeleteRequest(database, dbcursor, member)
            database.commit()
        elif(user_option == "6"):
            print("Logging out...")
            database.commit()
            database.close()
            time.sleep(1)
            os.system(cls)
            main()
        elif(user_option.upper() == "EXIT"):
            exitApp(database)
            # only way to properly exit the program
        else:
            print("Not a valid option, please try again")

def printInbox(database, dbcursor, member):
    dbcursor.execute("SELECT msgTimestamp, sender, content, rno FROM inbox WHERE email =\""+member+"\" AND seen = 'n' OR seen = 'N'")
    inbox = dbcursor.fetchall()
    if len(inbox) == 0:
        print("No unread messages to be displayed")
    else:
        for entry in inbox:
            print(entry)
    print('\n')
    dbcursor.execute("UPDATE inbox SET seen = 'y' WHERE seen = 'n' OR seen = 'N'")
        
def main():
    exiting = False
    dbname = input("Please enter the Database file name: ")
    database = sqlite3.connect(dbname)
    dbcursor = database.cursor()
            
    print("Welcome to Ride Finder")
    time.sleep(0.5)
    login_option = entry(database)
    if(login_option == 1):
        member = login(database, dbcursor)
    else:
        member = register(dbcursor)
        
    while not exiting:
        printInbox(database, dbcursor, member)
        mainMenu(database, dbcursor, member)
    # main activity, will continue to run unless explicitly exited

    if exiting:
        exitApp()
main()
