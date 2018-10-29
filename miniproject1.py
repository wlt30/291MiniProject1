import sys
import time
import sqlite3
import getpass
import os
import datetime

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
    print("LOGIN\nAt any point, type BACK to go back")
    while not validEmail:
        # receives user input for email and checks the validity of this email address in the database
        email = input("Email address: ")
        if(email.upper() == "EXIT"):
            exitApp()
        if(email.upper() == "BACK"):
            entry()
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
    os.system('cls')
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

def offerRide(dbcursor):
    os.system('cls')
    print("Offer a Ride")
    validDate = False
    validNoSeats = False
    validPricePerSeat = False
    validLugDesc = False
    validSrc = False
    validDst = False
    car_no = -1
    enroutes = []
    lcodes = getLCodes(dbcursor)
    cities = getCities(dbcuror)
    provs = getProvs(dbcursor)
    addresses = getAddresses(dbcursor)

    while not validDate:
        date = input("Enter ride date (e.g. 2018-01-01): ")
        if (len(date) != 10) or(date[4]!="-") or date(date[7]!='-'):
            print("Invalid date format, please try again (e.g. 2018-01-01)")
            continue
        else:
            validDate = True
    while not validNoSeats:
        noSeats = input("Enter the number of seats: ")
        try:
            noSeats = int(noSeats)
        except:
            print("Invalid input format, please try again ")
            continue
        validNoSeats = True
    while not validPricePerSeat:
        pricePerSeat = input("Enter a price per seat: ")
        try:
            pricePerSeat = int(pricePerSeat)
        except:
            print("Invalid input format, please try again ")
            continue
        validPricePerSeat = True
    while not validLugDesc:
        lugDesc = input("Enter a luggage description (max 10 characters): ")
        if len(lugDesc) >10 or len(lugDesc)==0:
            print("Invalid input format, please try again ")
            continue
        validLugDesc = True
    while not validSrc:
        src = input("Enter a source location (max 16 characters): ")
        if len(src) >5 or len(src)==0:
            print("Invalid input format, please try again ")
            continue
        srclcode = dbcursor.execute("SELECT lcode FROM locations WHERE lcode LIKE \"%"+entry+"%\"  OR city LIKE \"%"+entry+"%\" OR prov LIKE \"%"+entry+"%\" OR address LIKE \"%"+entry+"%\"")     
    while not validDst:
        dst = input("Enter a destination location (max 16 characters): ")
        if len(dst) >5 or len(dst)==0:
            print("Invalid input format, please try again ")
            continue
        validDst = True
        
    
def searchForRide(dbcursor):
    os.system('cls')
    print("Search for a Ride")
    
    
def bookMemberOrCancelBooking(dbcursor):
    os.system('cls')
    print("Book Member or Cancel Booking")
    
    
def postRideRequest(dbcursor):
    os.system('cls')
    print("Post Ride Request")
    
    
def searchAndDeleteRequest(dbcursor):
    os.system('cls')
    print("Search and Delete Ride Request")

def mainMenu(dbcursor, member):
    os.system('cls')
    exiting = False
    while not exiting:
        user_option = input("What would you like to do?\n1.Offer a Ride\n2.Search for Rides\n3.Book Members or Cancel Bookings\n4.Post Ride Request\n5.Search and Delete Ride Request\n6.Logout\nAt any point, type EXIT to end your session\n")
        if(user_option == "1"):
            time.sleep(1)
            offerRide(dbcursor)
        elif(user_option == "2"):
            time.sleep(1)
            searchForRide(dbcursor)
        elif(user_option == "3"):
            time.sleep(1)
            bookMemberOrCancelBooking(dbcursor)
        elif(user_option == "4"):
            time.sleep(1)
            postRideRequest(dbcursor)
        elif(user_option == "5"):
            time.sleep(1)
            searchAndDeleteRequest(dbcursor)
        elif(user_option == "6"):
            print("Logging out...")
            time.sleep(1)
            os.system('cls')
            main()
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
        member = login(dbcursor)
    else:
        member = register(dbcursor)
        database.commit()
    mainMenu(dbcursor, member)
    # main activity, will continue to run unless explicitly exited    
    if exiting:
        database.commit()
        database.close()
        exitApp()
main()
