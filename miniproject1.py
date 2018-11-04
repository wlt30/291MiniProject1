import sys
import time
import sqlite3
import getpass
import os
import datetime
import platform
import searchRides
import searchRequest

from datetime import datetime

def exitApp(database):
        os.system(cls)
        print('EXITING...\nThank you for using Ride Finder')
        time.sleep(2)
        database.commit()
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

def offerRide(dbcursor, member):
    os.system(cls)
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
                        src = srcOptions[int(choice)-1][0]
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
            src = srcOptions[0][0]
            print(srcOptions)
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
                        dst = dstOptions[int(choice)-1][0]
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
            dst = dstOptions[0][0]
            print(dstOptions)
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
            print(stopOptions)
        else:
            print("Sorry, we couldn't find any lcode, city, prov or address with that tag")


    while not validCar:
        cno = input("Please enter a car number or press ENTER to skip: ")
        if cno.isdigit():
            #prevents SQL injection because car_no cannot be "cno" and still get into this SQL call
            dbcursor.execute("SELECT cno, make, model, year, seats FROM cars WHERE cno = \"" +cno+ "\" AND owner = \"" +member+ "\"")
            cars = dbcursor.fetchone()
            if len(cars) == 0:
                print("That car was not found or does not belong to you, please try again")
                continue
            elif len(cars) == 1:
                validCar = True
                print(cars)
            else:
                print("Something went wrong, please try again")
                continue
        elif cno == "":
            validCar= True
            # only way to get out of loop
            cno = "NULL"
        else:
            print("Something went wrong, please try again")
            continue

    dbcursor.execute("INSERT INTO rides VALUES (\""+rno+"\", \""+pricePerSeat+"\", \""+date+"\", \""+noSeats+"\", \""+lugDesc+"\", \""+str(src)+"\", \""+str(dst)+"\", \""+driver+"\", \""+cno+"\")")
    for item in enroutes:
        dbcursor.execute("INSERT INTO enroute VALUES (\"" +rno+"\", \""+item[0]+"\")")
    os.system(cls)

def searchForRide(dbcursor):
    os.system(cls)
    print("Search for a Ride")

#Working on bookings
def Bookings(dbcursor,member): #Assume member passed it the user email logged on
    os.system(cls)
    Finished = False
    while not Finished:
        user_input= input("What would you like to do?\n1.List all bookings on ride user offers\n2.Cancel Bookings on rides user offer\n3.List All rides user offers and number of availble seats for each ride \n4.Book Rides\n5.Finished\n")

        if(user_input == "1"):
            print("-------------List All rides member offers and number of availble seats for each ride -------------\n");
            print("member is: ", member, "\n")
            dbcursor.execute("SELECT b.bno, r.rno, r.driver, b.email FROM bookings b, rides r WHERE r.rno = b.rno and r.driver = ?\n", (member,)) #multiple rno, but with differrnt bno tags
            Booking = dbcursor.fetchall() #all results will be stored into the list of tuples in Bookings

            i = 0;
            for row in Booking:
                print("|bno: %s|rno: %s|driver: %s|passenger: %s|\n"%(str(row[0]), str(row[1]), str(row[2]), str(row[3])))
                i = i+1;
                if i%5 ==0:
                    more = input("Print more Bookings offered (yes/no)\n")
                    if more.lower() == "no":
                        break
                    else:
                        continue
            print("-------------Finished Listing Bookings-------------")
            #Proceed with listing other  member rides afterwards, except current member
        elif (user_input =="2"):
            print("-------------Cancel Bookings on Rides user Offers-------------")

            #-------------------------------Test-------------------------------
            # dbcursor.execute("SELECT r.rno, b.bno, r.driver FROM bookings b, rides r where r.rno =b.rno and r.driver =?;", (member,))
            # test= dbcursor.fetchall()
            # for each in test:
            #     print(each)
            #------------------------------------------------------------------

            check = False
            while check == False:
                bno = int(input("Enter bno: ")) #
                dbcursor.execute("SELECT b.bno FROM bookings b, rides r where r.rno =b.rno and b.bno = ? and r.driver =?;",(bno,member,))
                if dbcursor.fetchone() == None:
                    print("Bno Does not exist Try Again: ")
                else:
                    print("Bno Entered is: rno: ",  bno)
                    dbcursor.execute("select b.email, b.rno from bookings b where b.bno =?", (bno,))
                    data = dbcursor.fetchone()
                    email = data[0]
                    rno = data[1]
                    print("Email: ", email, "Rno: ", rno)


                    print(email)

                    dbcursor.execute("Delete from bookings where bno = ?", (bno,))

                    dbcursor.execute("INSERT into inbox values(?,?,?,?,?,?);",(email, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),member,"Your booking Has been cancelled",rno,'n',))
                    dbcursor.execute("Select * from inbox")
                    ya =dbcursor.fetchall()
                    for each in ya:
                        print(each)

                    check =True




        elif(user_input == "3"):
            print("-------------List All rides member offers and number of availble seats for each ride -------------\n");
            print("member is: ", member, "\n")
            #Your system should list all rides the member offers with the number of available seats for each ride (i.e., seats that are not booked).
            #Include rides that have bookings and rides that do not have bookings  [r.rno = b.rno]

            #dbcursor.execute(" SELECT b.bno,r.rno,r.driver, b.email, r.seats, b.seats FROM bookings b, rides r WHERE r.driver = ? and r.rno<>b.rno UNION SELECT b.bno,r.rno,r.driver, b.email, r.seats, b.seats FROM bookings b, rides r WHERE r.driver =? and r.rno=b.rno", (member,member,))
            print("SWAG")
            dbcursor.execute("SELECT b.bno, r.rno, r.driver, b.email, r.seats, b.seats FROM bookings b, rides r where r.rno = b.rno and r.driver = ?\n", (member,)) #multiple rno, but with differrnt bno tags
            Booking = dbcursor.fetchall() #all results will be stored into the list of tuples in Bookings

            i = 0;
            for row in Booking:
                print("|bno: %s|rno: %s|driver: %s|passenger: %s|Ride Seats: %s|Seats Booked: %s|Seats available: %s|\n"%(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(int(row[4] - int(row[5]))) ))
                i = i+1;
                if i%5 ==0:
                    more = input("Print more Rides offered (yes/no)\n")
                    if more.lower() == "no":
                        break
                    else:
                        continue
            print("-------------Finished Listing Bookings-------------")



        elif(user_input =="4"):       #selects rno from all rides of ride table, As long as its inputed correctly it should be fine
            print("-------------Booking Rides-------------")
            check1 = False
            while check1 == False:
                rno = int(input("Enter Rno: ")) #
                dbcursor.execute("SELECT rno FROM rides where rno = ?;",(rno,))
                if dbcursor.fetchone() == None:
                    print("Rno Does not exist Try Again: ")
                else:
                    print("Rno Entered is: rno: ",  rno)
                    check1 =True

            check2 = False
            while check2 ==False:
                email =input("Enter Email: ")
                dbcursor.execute("Select email FROM Members where email =?;",(email,))
                if dbcursor.fetchone() == None:  #check if none first if not none check if the email match rno
                    print("Email does not exist Try Again: ")
                else:
                    print("Emial Entered is: ", email)
                    check2 = True

            check3 = False
            while check3 ==False:
                pickup = input("Enter pickup Location code: ")
                dbcursor.execute("Select lcode from locations where lcode = ?;", (pickup,))
                if dbcursor.fetchone() == None:
                    print("lcode for pick up does not exist Try Again")
                else:
                    print("lcode entered is: ", pickup)
                    check3 = True

            check4 = False
            while check4 ==False:
                dropoff = input("Enter Drop off location: ")
                dbcursor.execute("Select lcode from locations where lcode = ?;", (dropoff,))
                if dbcursor.fetchone() == None:
                    print('lcode for drop off does not exist Try Again')
                else:
                    print("lcode for dropoff entered is: ", dropoff)
                    check4 = True

            check5 = False
            while check5 == False:
                cost = int(input("Enter Cost per seat: "))      #accepts integer
                dbcursor.execute("Select price from rides where rno =?;", (rno,))
                if cost != dbcursor.fetchone()[0]:
                    print("Cost for ride is not correct please Try Again")
                else:
                    print("Cost entered per seat: ", cost)
                    check5 = True

            check6 = False
            dbcursor.execute("Select seats from rides where rno = ?;", (rno,))
            seat_check = dbcursor.fetchone()[0]
            dbcursor.execute("Select seats from bookings where rno =? ", (rno,))
            already_book = dbcursor.fetchone()
            if already_book ==None:
                already_book = 0
            else:
                already_Booked = already_booked[0]     #Changed
            print("Seats Entere:", seat_check)
            print("already Booked: ", already_Booked)
            seat_check = seat_check - already_Booked
            print("Seats Available: ", seat_check)
            dbcursor.execute("Select bno from bookings")
            bno =  dbcursor.fetchall()[-1][0] +1 #Unique bno = last bno +1
            print("Last bno is: ", (bno-1), "New bno is: ", bno)


            while check6 == False:
                seatsbook = int(input("Enter amount of seats you want to book: "))
                if  (seat_check - seatsbook) < 0:
                    choice = input("The number of seats booked exceeds the number of seats offered\nDo you Want to continue to book the ride? (yes/no) ")
                    if choice.lower() == "yes":
                        print("You have confirmed your bookings")
                        # CREATE SQL to update to the table
                        dbcursor.execute("INSERT into Bookings values(?,?,?,?,?,?,?);",(bno,email,rno,cost,seatsbook,pickup,dropoff))
                        print("A msg has sent to member who's ride has been booked")

                        # dbcursor.execute("Select * from Bookings;")
                        # inbox = dbcursor.fetchall()
                        # for each in inbox:
                        #     print(each)

                        #Test Inbox Sent-------------------
                        # dbcursor.execute("Select * from inbox;")
                        # inbox = dbcursor.fetchall()
                        # for each in inbox:
                        #     print(each)
                        #

                        dbcursor.execute("INSERT into inbox values(?,?,?,?,?,?);",(email, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),member,"New Booking",rno,'n',))

                        # dbcursor.execute("Select * from inbox;")
                        # inbox2 = dbcursor.fetchall()
                        # for each in inbox2:
                        #     print(each)
                        #Test Inbox Sent------------------

                        check6 =True
                    elif choice.lower() == "no":
                        print("No ride has been booked\nThank you")
                        check6 = True
                else:
                    dbcursor.execute("INSERT into Bookings values(?,?,?,?,?,?,?)",(bno,email,rno,cost,seatsbook,pickup,dropoff))

                    print("Your ride has been booked!\n A msg has been sent to the member who's ride has been booked  ")
                    check6 =True

            #how can i take take in mulltiple inputs at the same time
            #Check if seats going to be book > seats offered



            # The member should be able to select a ride and book a member for that ride by entering the member email, the number of seats booked, the cost per seat, and pickup and drop off location codes. Your system should assign a unique booking number (bno) to the booking. Your system should give a warning if a ride is being overbooked (i.e. the number of seats booked exceeds the number of seats offered), but will allow overbooking if the member confirms it. After a successful booking, a proper message should be sent to the other member that s/he is booked on the ride.

        elif(user_input == "5"):
            print("Returning to the Main Menu\n")
            Finished = True



def postRideRequest(dbcursor,member):
    os.system(cls)
    print("Post Ride Request")
    rdate = input("Enter Return Date (YYYY-MM-DD): ")

    check1 = False
    while check1 ==False:
        pickup = input("Enter pickup Location code: ")
        dbcursor.execute("Select lcode from locations where lcode = ?;", (pickup,))
        if dbcursor.fetchone() == None:
            print("lcode for pick up does not exist Try Again")
        else:
            print("lcode entered is: ", pickup)
            check1 = True

    check2 = False
    while check2 ==False:
        dropoff = input("Enter dropoff Location code: ")
        dbcursor.execute("Select lcode from locations where lcode = ?;", (dropoff,))
        if dbcursor.fetchone() == None:
            print("lcode for dropoff does not exist Try Again")
        else:
            print("lcode entered is: ", dropoff)
            check2 = True



    amount = input("Enter amount willing to pay per seat: ")
#-----------------------TEST----------------------
    dbcursor.execute("Select * from requests")
    requests = dbcursor.fetchall()
    print("Requsets Before members adds")
    for each in requests:
        print(each)
#-------------------------------------------------
    dbcursor.execute("Select rid from requests")
    rid =  dbcursor.fetchall()[-1][0] +1 #Unique bno = last bno +1

    #requests(rid, email, rdate, pickup, dropoff, amount)
    dbcursor.execute("INSERT into requests VALUES(?,?,?,?,?,?)", (rid,member, rdate, pickup, dropoff, amount,))

#-----------------------TEST----------------------
    dbcursor.execute("Select * from requests")
    requests2 = dbcursor.fetchall()
    print("\nRequsets Before members adds")
    for each in requests2:
        print(each)
#-------------------------------------------------


def searchAndDeleteRequest(dbcursor):
    os.system(cls)
    print("Search and Delete Ride Request")

def mainMenu(database, dbcursor, member):
    os.system(cls)
    exiting = False
    while not exiting:
        user_option = input("What would you like to do?\n1.Offer a Ride\n2.Search for Rides\n3.Book Members or Cancel Bookings\n4.Post Ride Request\n5.Search and Delete Ride Request\n6.Logout\nAt any point, type EXIT to end your session\n")
        if(user_option == "1"):
            time.sleep(0.5)
            offerRide(dbcursor, member)
            database.commit()
        elif(user_option == "2"):
            time.sleep(0.5)
            searchRides.searchForRide(database, dbcursor, member)
        elif(user_option == "3"):

            time.sleep(0.5)
            Bookings(dbcursor,member)
        elif(user_option == "4"):
            time.sleep(0.5)
            postRideRequest(dbcursor, member)
        elif(user_option == "5"):
            time.sleep(0.5)
            searchRequest.searchAndDeleteRequest(database, dbcursor, member)
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

if((platform.system()) == "Windows"):
    cls = 'cls'
elif((platform.system()) == "Linux"):
    cls = 'clear'
elif((platform.system()) == "Darwin"):
    cls = 'clear'

def main():
    exiting = False
    validDatabase = False
    while not validDatabase:
        dbname = input("Please enter the Database file name: ")
        database = sqlite3.connect(dbname)
        dbcursor = database.cursor()
        try:
            dbcursor.execute("SELECT * FROM members")
        except:
            print("Invalid/empty database, please try again")
            continue
        members = dbcursor.fetchall()
        if len(members) == 0:
                print("Invalid/empty database, please try again")
                continue
        else:
            validDatabase = True

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
        database.commit()
    # main activity, will continue to run unless explicitly exited

    if exiting:
        database.commit()
        database.close()
        exitApp()
main()
