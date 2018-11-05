import sys
import time
import sqlite3
import getpass
import os
import datetime
import platform


from datetime import datetime

if((platform.system()) == "Windows"):
    cls = 'cls'
elif((platform.system()) == "Linux"):
    cls = 'clear'
elif((platform.system()) == "Darwin"):
    cls = 'clear'

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
            print("-------------Listing All rides member offers and number of availble seats for each ride -------------\n");

            print("member is: ", member, "\n")
            dbcursor.execute("SELECT b.bno, r.rno, r.driver, b.email, r.seats, b.seats FROM bookings b, rides r where r.rno = b.rno and r.driver = ?\n", (member,)) #multiple rno, but with differrnt bno tags
            Booking = dbcursor.fetchall() #all results will be stored into the list of tuples in Bookings
            i = 0;
            for row in Booking:
                print("-------------Listing Rides with Bookings -------------\n");
                print("|bno: %s|rno: %s|driver: %s|passenger: %s|Ride Seats: %s|Seats Booked: %s|Seats available: %s|\n"%(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(int(row[4] - int(row[5]))) ))
                i = i+1;
                if i%5 ==0:
                    more = input("Print more Rides offered (yes/no)")
                    if more.lower() == "no":
                        break
                    else:
                        continue
            dbcursor.execute("SELECT r.rno, r.driver, r.seats from rides r where r.driver =? EXCEPT SELECT r.rno, r.driver, r.seats from rides r, bookings b where r.driver =? and b.rno=r.rno", (member,member,))
            no_bookings = dbcursor.fetchall();
            if len(no_bookings) == 0:
                print("There are no ride with no bookings")
            else:
                print("-------------Listing Rides with no Bookings -------------\n")
                for each in no_bookings:
                    print("|rno: %s|driver: %s|seats Booked: %s|Seats available: %s|"%(each[0], each[1],each[2],each[2]))




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
                    print("Email Entered is: ", email)
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
                already_book = already_book[0]     #Changed
            print("Seats Entere:", seat_check)
            print("already Booked: ", already_book)
            seat_check = seat_check - already_book
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

