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

def postRideRequest(dbcursor,member):
    os.system(cls)
    print("Post Ride Request")
    validDate = False
    rdate = input("Enter Return Date (YYYY-MM-DD): ")
    while not validDate:
        date = input("Enter Return Date (e.g. YYYY-MM-DD): ")
        if (len(rdate) != 10) or (rdate[4]!="-") or (rdate[7]!='-') or not (rdate[0:4].isdigit()) or not (rdate[5:7].isdigit()) or  not (rdate[8:10].isdigit()):
            print("Invalid date format, please try again (e.g. YYYY-MM-DD)")
            continue
        else:
            year = int(rdate[0:4])
            month = int(rdate[5:7])
            day = int(rdate[8:10])
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
