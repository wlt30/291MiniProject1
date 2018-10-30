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

def offerRide(dbcursor, member):
    os.system('cls')
    print("Offer a Ride")
    driver = str(member)
    dbcursor.execute("SELECT MAX(rno) FROM rides")
    rno = str(int(dbcursor.fetchone()[0]) + 1)
    validDate = False
    validNoSeats = False
    validPricePerSeat = False
    validLugDesc = False
    validSrc = False
    validDst = False
    validCar = False
    validEnroutes = False
    enroutes = []

    while not validDate:
        date = input("Enter ride date (e.g. YYYY-MM-DD): ")
        if (len(date) != 10) or (date[4]!="-") or (date[7]!='-') or not (date[0:4].isdigit()) or not (date[5:7].isdigit()) or  not (date[8:10].isdigit()):
            print("Invalid date format, please try again (e.g. YYYY-MM-DD)")
            continue
        else:
            year = int(date[0:4])
            month = int(date[5:7])
            day = int(date[8:10])
            if (month > 12) or (month < 1) or (day < 1) or (day>31):
                print("Invalid date format, please try again (e.g. YYYY-MM-DD)")
                continue
            if(month==4)or(month==6)or(month==9)or(month==11):
                if day>30:
                    print("Invalid date format, please try again (e.g. YYYY-MM-DD)")
                    continue
            if(month==2):
                if(year%4 == 0):
                    if day>29:
                        print("Invalid date format, please try again (e.g. YYYY-MM-DD)")
                        continue
                elif day>28:
                    print("Invalid date format, please try again (e.g. YYYY-MM-DD)")
                    continue
            validDate = True
                                                                                                
    while not validNoSeats:
        noSeats = input("Enter the number of seats: ")
        if noSeats.isdigit():
            validNoSeats = True
        else:
            print("Invalid input format, please try again ")
            continue
                                                                                                
    while not validPricePerSeat:
        pricePerSeat = input("Enter a price per seat: ")
        if pricePerSeat.isdigit():
            validPricePerSeat = True
        else:
            print("Invalid input format, please try again ")
            continue
        
                                                                                                
    while not validLugDesc:
        lugDesc = input("Enter a luggage description (max 10 characters): ")
        if len(lugDesc) >10 or len(lugDesc)==0:
            print("Invalid input format, please try again ")
            continue
        validLugDesc = True
                                                                                                
    while not validSrc:
        entry = input("Enter a source location (max 16 characters): ")
        if len(entry) >16 or len(entry)==0:
            print("Invalid input format, please try again ")
            continue
        dbcursor.execute("SELECT * FROM locations WHERE lcode LIKE \"%"+entry+"%\"  OR city LIKE \"%"+entry+"%\" OR prov LIKE \"%"+entry+"%\" OR address LIKE \"%"+entry+"%\"")
        srcOptions = dbcursor.fetchall()
        x = 0
        if(len(srcOptions)>1):
            print("Please select source location by option number or press ENTER for more options")
            while x < len(srcOptions):
                try:
                    print(str(x+1) +". " +str(srcOptions[x]))
                    x = x+1
                except:
                    continue
                if x//5 > 0:
                    choice = input("")
                    if choice.isdigit():
                        src = srcOptions[int(choice)-1]
                        validSrc = True
                        break
                    elif choice == "":
                        if x+1 > len(srcOptions):
                            x = 0
                        continue
                    else:
                        print("Invalid choice, please try again")
                        x = 0
                        continue    
        elif(len(srcOptions)==1):
            src = srcOptions[0]
            validSrc = True
        else:
            print("Sorry, we couldn't find any lcode, city, prov or address with that tag")
            continue
    
    while not validDst:
        entry = input("Enter a destination location (max 16 characters): ")
        if len(entry) >16 or len(entry)==0:
            print("Invalid input format, please try again ")
            continue
        dbcursor.execute("SELECT * FROM locations WHERE lcode LIKE \"%"+entry+"%\"  OR city LIKE \"%"+entry+"%\" OR prov LIKE \"%"+entry+"%\" OR address LIKE \"%"+entry+"%\"")
        dstOptions = dbcursor.fetchall()
        x = 0
        if(len(dstOptions)>1):
            print("Please select destination location by option number or press ENTER for more options")
            while x < len(dstOptions):
                try:
                    print(str(x+1) +". " +str(dstOptions[x]))
                    x = x+1
                except:
                    continue
                if x//5 > 0:
                    choice = input("")
                    if choice.isdigit():
                        dst = dstOptions[int(choice)-1]
                        validDst = True
                        break
                    elif choice == "":
                        if x+1 > len(dstOptions):
                            x = 0
                        continue
                    else:
                        print("Invalid choice, please try again")
                        x = 0
                        continue    
        elif(len(dstOptions)==1):
            dst = dstOptions[0]
            validDst = True
        else:
            print("Sorry, we couldn't find any lcode, city, prov or address with that tag")


    while not validEnroutes:
        stop = input("Enter an enroute location (max 16 characters) or press ENTER to continue: ")
        if len(stop) >16:
            print("Invalid input format, please try again ")
            continue
        if stop == "":
            validEnroutes = True
            ## only way to pass this step
            continue
        
        dbcursor.execute("SELECT * FROM locations  WHERE lcode LIKE \"%"+stop+"%\"  OR city LIKE \"%"+stop+"%\" OR prov LIKE \"%"+stop+"%\" OR address LIKE \"%"+stop+"%\"")
        stopOptions = dbcursor.fetchall()
        x = 0
        if(len(stopOptions)>1):
            print("Please select enroute location by option number or press ENTER for more options")
            while x < len(stopOptions):
                try:
                    print(str(x+1) +". " +str(stopOptions[x]))
                    x = x+1
                except:
                    continue
                if x//5 > 0:
                    choice = input("")
                    if choice.isdigit():
                        stop = stopOptions[int(choice)-1]
                        enroutes.append(stop)
                        break
                    elif choice == "":
                        if x+1 > len(stopOptions):
                            x = 0
                        continue
                    else:
                        print("Invalid choice, please try again")
                        x = 0
                        continue    
        elif(len(stopOptions)==1):
            enroutes.append(stopOptions[0])
        else:
            print("Sorry, we couldn't find any lcode, city, prov or address with that tag")
        

    while not validCar:
        cno = input("Please enter a car number or press ENTER to skip: ")
        if cno.isdigit():
            #prevents SQL injection because car_no cannot be "cno" and still get into this SQL call
            dbcursor.execute("SELECT cno FROM cars WHERE cno = \"" +cno+ "\"")
            cars = dbcursor.fetchall()
            if len(cars) == 0:
                print("That car was not found, please try again")
                continue
            elif len(cars) == 1:
                validCar = True
            else:
                print("Something went wrong, please try again")
                continue
        elif cno == "":
            validCar= True
            cno = "NULL"
        else:
            print("Something went wrong, please try again")
            continue

    dbcursor.execute("INSERT INTO rides VALUES (\""+rno+"\", \""+pricePerSeat+"\", \""+date+"\", \""+noSeats+"\", \""+lugDesc+"\", \""+str(src)+"\", \""+str(dst)+"\", \""+driver+"\", \""+cno+"\")")
    
                
        
    
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
            time.sleep(0.5)
            offerRide(dbcursor, member)
        elif(user_option == "2"):
            time.sleep(0.5)
            searchForRide(dbcursor)
        elif(user_option == "3"):
            time.sleep(0.5)
            bookMemberOrCancelBooking(dbcursor)
        elif(user_option == "4"):
            time.sleep(0.5)
            postRideRequest(dbcursor)
        elif(user_option == "5"):
            time.sleep(0.5)
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
    time.sleep(0.5)
    login_option = entry()
    if(login_option == 1):
        member = login(dbcursor)
    else:
        member = register(dbcursor)
        database.commit()
    while not exiting:
        mainMenu(dbcursor, member)
        database.commit()
    # main activity, will continue to run unless explicitly exited    
    if exiting:
        database.commit()
        database.close()
        exitApp()
main()
