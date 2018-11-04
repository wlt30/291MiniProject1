import sys
import time
import sqlite3
import getpass
import os
import datetime

def messageOwner(dbcursor, rideindex, displayedrides, member):
    os.system('clear')
    os.system('clear') #make sure the entire terminal screen is flushed

    #get the indicated ride and the owner of that ride.
    ride = displayedrides[rideindex]
    #ride should have format [rno, price, rdate, seats, lugDesc, src, dst, driver]
    owner = ride[7]
    rno = ride[0]
    database = sqlite3.connect('testDatabase.db')
    dbcursor = database.cursor()

    #prompt the reader to enter a new email message to the owner
    fetch = input(("Enter a new message for {} or type BACK to return to search\n").format(owner))

    if fetch.upper() == 'BACK':
        os.system('clear')
        return

    elif fetch.upper() == 'EXIT': # if the user wants to exit
        os.system("clear")
        print('EXITING\nThank you for using this Ride Finder')
        time.sleep(2)
        os.system('clear')
        sys.exit()

    else:
        #insert a new message into the table
        dbcursor.execute((
            "INSERT INTO inbox VALUES (?, datetime('now'), ?, ?, ?, 'n')"), (owner, member, fetch, rno))

        print("Message sent...")

    print("Returning to Search")
    database.commit()
    time.sleep(2)

    return


def searchForRide(dbcursor, member):

    while(1):
        #os.system('clear')
        userInput = input("Please enter up to three keywords or type BACK to leave: ")
        ridelist = []  # will contain all rides that match the keywords
        os.system('clear')

        if userInput.upper()== "EXIT":
            os.system("clear")
            print('EXITING\nThank you for using this Ride Finder')
            time.sleep(2)
            os.system('clear')
            sys.exit()

        elif userInput.upper() == "BACK":
            os.system("clear")
            return

        keywords = userInput.split(" ")
        keywords = list(filter(None, keywords)) #filtering list https://stackoverflow.com/questions/16099694/how-to-remove-empty-string-in-a-list/16099706
        if len(keywords) > 3 or len(keywords) < 1:
            print("Invalid number of arguments")
            continue

        #For each line we want to query all rides with the relevant key words
        for word in keywords:
            temporaryridelist = []
            keywordString = word

            #Lets check if it is a relevant location code for source
            queryString = ("SELECT rno, price, rdate, seats, lugDesc, l1.city, l2.city, driver, cno FROM locations l1, locations l2, rides \
                                                   WHERE l1.lcode LIKE ? AND l1.lcode = src AND l2.lcode = dst")  #LIKE is case insensitive
            dbcursor.execute(queryString,(keywordString,)) #prevent sql injection
            results = dbcursor.fetchall()
            temporaryridelist = temporaryridelist + results #append the results to ride list

            #check if it is a relevant location code for destination
            queryString = ("SELECT rno, price, rdate, seats, lugDesc, l2.city, l1.city, driver, cno FROM locations l1, locations l2, rides \
                                       WHERE l1.lcode LIKE ? AND l1.lcode = dst AND l2.lcode = src")  # LIKE is case insensitive
            dbcursor.execute(queryString, (keywordString,))
            results = dbcursor.fetchall()
            temporaryridelist = temporaryridelist + results

            # check if it is a relevant location code for enroute rides
            queryString = ("SELECT r.rno, r.price, r.rdate, r.seats, r.lugDesc, l1.city, l2.city, r.driver, r.cno FROM locations l1, locations l2, rides r, enroute e \
                                                   WHERE  e.lcode LIKE ? AND e.rno = r.rno AND l1.lcode = r.src AND l2.lcode = r.dst")  # LIKE is case insensitive
            dbcursor.execute(queryString, (keywordString,))
            results = dbcursor.fetchall()
            temporaryridelist = temporaryridelist + results
            keywordString = '%%' + word + '%%'

            #check if keyword is a substring of city, province, or address for source
            queryString = (("SELECT rno, price, rdate, seats, lugDesc, l1.city, l2.city, driver, cno FROM locations l1, locations l2, rides" 
                           " WHERE (l1.city LIKE ? OR l1.prov LIKE ? OR l1.address LIKE ?)"
                           " AND l1.lcode = src AND l2.lcode = dst"))

            dbcursor.execute(queryString, (keywordString, keywordString, keywordString)) #protect against SQL injection
            results = dbcursor.fetchall()
            temporaryridelist = temporaryridelist + results
            #check if keyword is a substring of city, province or address for destination
            queryString = ((
                "SELECT rno, price, rdate, seats, lugDesc, l2.city, l1.city, driver, cno FROM locations l1, locations l2, rides" 
                " WHERE (l1.city LIKE ? OR l1.prov LIKE ? OR l1.address LIKE ?)"
                " AND l1.lcode = dst AND l2.lcode = src"))

            dbcursor.execute(queryString, (keywordString, keywordString, keywordString)) #prevent sql injection
            results = dbcursor.fetchall()
            temporaryridelist = temporaryridelist + results

            ##at the end of querying, we should compare the temporary ride list with the rides currently in the actual ride list
            ##Only keep the ones that are in both lists (i.e if there are multiple keywords take the set intersection of each keyword list)
            if not ridelist:
                #if the list is currently empty just set the temp list as the ridelist
                ridelist = list(set(ridelist + temporaryridelist)) #set gets rid of duplicates

            #compare the two lists and only take the intersection https://stackoverflow.com/questions/2864842/common-elements-comparison-between-2-lists
            else:
                ridelist = list(set(ridelist) - (set(ridelist) - set(temporaryridelist))) #set also removes duplicates


        #if no results were returned
        if len(ridelist) == 0:
            print("No results found")
            time.sleep(2)
            os.system('clear')
            continue
        #print the results (only do 5 at a time)
        while len(ridelist) != 0:
            displayedrides = [] #contains rides currently on display, will be used for when user wants to choose a ride

            print("Returning Search Results \n")
            for x in range(1,6):
                if len(ridelist) == 0:
                    break
                ride = ridelist.pop()
                displayedrides.append(ride) #add to list of currently displayed rides
                print(("{}. Ride Number: {}, Price: {}, Date: {}\nSeats Available: {}, Luggage Allowance: {}" 
                "\nFROM: {}, TO: {}, Driver: {}\n").format(x, ride[0], ride[1], ride[2], ride[3], ride[4], ride[5], ride[6], ride[7]))

                if ride[8] is None:
                    #Let the user know there is no car information available
                    print("No car information available at this time \n\n")

                else:
                    #query for car information and print it
                    querystring = ("SELECT make, model, year, seats, owner FROM cars WHERE cno = {}").format(ride[8])
                    dbcursor.execute(querystring)
                    carinfo = dbcursor.fetchall()
                    carinfo = carinfo.pop()
                    print(("Car Information\nMake: {}, Model: {}, Year: {}, Seats: {}, Owner Email: {}\n\n").format(carinfo[0], carinfo[1],
                                                                                                                carinfo[2], carinfo[3], carinfo[4]))


            #check if user wants to get the next results or have them select an index to message the ride owner
            if len(ridelist) != 0:
                fetch = input("There Are More Results. Type MORE to see more results, RETURN to return to searching, or type ride index to message driver\n")

                if fetch.upper() == 'MORE':
                    os.system('clear')
                    os.system('clear')
                    os.system('clear') #CLEAR ONLY CLEARS WHAT IS VISIBLE. I DO THIS 3 TIMES TO ENSURE ENTIRE WINDOW IS CLEARED
                    continue


                elif fetch.upper() == 'RETURN':
                    os.system('clear')
                    break

                elif '1' <= fetch <= '5':
                    #the user wants to message the owner of the ride
                    messageOwner(dbcursor, int(fetch) - 1, displayedrides, member)
                    break

                elif fetch.upper() == 'EXIT':
                    os.system("clear")
                    print('EXITING\nThank you for using this Ride Finder')
                    time.sleep(2)
                    os.system('clear')
                    sys.exit() #if user wants to exit

                elif fetch.upper() == 'BACK':
                    os.system('clear') #if the user wants to go back to main menu
                    return

                else:
                    os.system('clear')
                    print("invalid input\n")
                    time.sleep(2)
                    os.system('clear')
                    break

        if len(ridelist) != 0: #this case occurs if the user returned before seeing all the rides. in this case return to beginning
            continue

        #Prompt user to choose a ride or exit
        fetch = input("Type RETURN to return to searching, or type ride index to message driver\n")
        if fetch.upper() == 'RETURN':
            os.system('clear')
            continue

        elif '1' <= fetch <= str(len(displayedrides)):
            #user wants to message owner
            messageOwner(dbcursor, int(fetch) - 1, displayedrides, member)
            continue;

        elif fetch.upper() == 'BACK':
            os.system('clear')  # if the user wants to go back to main menu
            return

        elif fetch.upper() == 'EXIT':
            os.system("clear")
            print('EXITING\nThank you for using this Ride Finder')
            time.sleep(2)
            os.system('clear')
            sys.exit()  # if user wants to exit



        else:
            print("invalid input.. returning to search\n")
            time.sleep(2)
            os.system('clear')
            continue;
    return
