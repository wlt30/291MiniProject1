import sys
import time
import sqlite3
import getpass
import os
import datetime


def searchForRide(dbcursor):
    print("Searching for Rides...")
    ridelist= [] #will contain all rides that match the keywords
    while(1):
        userInput = input("Please enter up to three keywords or type BACK to leave: ")

        if userInput.upper()== "EXIT":
            os.system("clear")
            print('EXITING\nThank you for using this Ride Finder')
            time.sleep(2)
            sys.exit()

        keywords = userInput.split(" ")

        if len(keywords) > 3 or len(keywords) < 1:
            print("Invalid number of arguments")
            continue

        #For each line we want to query all rides with the relevant key words
        for word in keywords:
            #Lets check if it is a relevant location code for source
            queryString = ("SELECT rno, price, rdate, seats, lugDesc, l1.city, l2.city, driver, cno FROM locations l1, locations l2, rides \
                                                   WHERE l1.lcode = '%s' AND l1.lcode = src AND l2.lcode = dst" % word)  #LIKE is case insensitive
            dbcursor.execute(queryString)
            results = dbcursor.fetchall()
            ridelist = ridelist + results #append the results to ride list

            queryString = ("SELECT rno, price, rdate, seats, lugDesc, l2.city, l1.city, driver, cno FROM locations l1, locations l2, rides \
                                       WHERE l1.lcode = '%s' AND l1.lcode = dst AND l2.lcode = src" % word)  # LIKE is case insensitive
            dbcursor.execute(queryString)
            results = dbcursor.fetchall()
            ridelist = ridelist + results  # do the same but check if it matches dst lcode

            queryString = ("SELECT rno, price, rdate, seats, lugDesc, l1.city, l2.city, driver, cno FROM locations l1, locations l2, rides \
                                                               WHERE l1.lcode = '%s' AND l1.lcode = src AND l2.lcode = dst" % word)  # LIKE is case insensitive
            dbcursor.execute(queryString)
            results = dbcursor.fetchall()
            ridelist = ridelist + results  # append the results to ride list

            queryString = ("SELECT rno, price, rdate, seats, lugDesc, l2.city, l1.city, driver, cno FROM locations l1, locations l2, rides \
                                                   WHERE l1.lcode = '%s' AND l1.lcode = dst AND l2.lcode = src" % word)  # LIKE is case insensitive
            dbcursor.execute(queryString)
            results = dbcursor.fetchall()
            ridelist = ridelist + results  

        #if no results were returned
        if len(ridelist) == 0:
            print("No results found")
            os.system('clear')
            continue
        #print the results (only do 5 at a time)
        while len(ridelist) != 0:
            print("Returning Search Results \n")
            for x in range(1,6):
                if len(ridelist) == 0:
                    continue;
                ride = ridelist.pop()
                print(("Ride Number: {}, Price: {}, Date: {}, Seats Available: {}, Luggage Allowance: {}" 
                "\nFROM: {}, TO: {}, Driver: {}, Car: {}\n").format(ride[0], ride[1], ride[2], ride[3], ride[4], ride[5], ride[6], ride[7], ride[8]))

            #check if user wants to get the next results
            if len(ridelist) != 0:
                fetch = input("There Are More Results. Fetch next Results? Y/N\n")

                if fetch.upper() == 'Y':
                    os.system('clear')
                    continue;

                else:
                     break;



    return
