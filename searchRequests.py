##This file is used to handle task 5 of the specification: search/delete requests
##There are two main streams to consider:
##1. whether the user wants to view/delete their own requests
##2. whether the user wants to view other requests and message the poster

import sys
import time
import sqlite3
import getpass
import os
import datetime

def messageRequestOwner(index, displayedRequests, member):
    ##When the user searches for request and wants to message owner we call this function
    ##this will create a new row in the inbox table
    os.system('clear')
    os.system('clear')  # make sure the entire terminal screen is flushed

    #We also need the user to specify what ride number is related to the message
    fetch = input("What ride number do you want to associate with the message?\n")

    try:
        rno = int(fetch)

    except ValueError: #https://stackoverflow.com/questions/27310631/checking-if-input-is-an-integer
        print("Not a number! Returning to request screen...")
        time.sleep(3)
        return

    #now check if the ride actually exists
    queryString = ("SELECT rno, driver FROM rides WHERE rno = {}").format(rno)

    database = sqlite3.connect('testDatabase.db')
    dbcursor = database.cursor()
    dbcursor.execute(queryString)
    result = dbcursor.fetchall()

    if len(result) == 0: #if ride does not exist then return
        print("Ride does not exist! Returning to request screen...")
        time.sleep(3)
        return

    #Now we can send the message
    # get the indicated ride and the owner of that ride.
    request = displayedRequests[index]
    # request should have format rid, email, rdate, pickup, dropoff
    poster = request[1]
    fetch = input(("What message would you like to send to {}?\n").format(poster))

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
        # insert a new message into the table
        dbcursor.execute(("INSERT INTO inbox VALUES ('{}', datetime('now'), "
                          "'{}', '{}', {}, 'n')").format(poster, member, fetch, rno))

        print("Message sent...")

    print("Returning to Request Screen")
    database.commit()
    time.sleep(2)
    return

def deleteRequest(index, displayedRequests):
    ##this function is used to delete a row from the sqlite database
    ##the user selected which request from the screen they wanted to delete
    ##index and displayed requests tracks which request is the one they selected

    database = sqlite3.connect('testDatabase.db')
    dbcursor = database.cursor()
    request = displayedRequests[index]

    #create the command and execute it
    #request should have format rid, email, rdate, pickup, drop off

    #ask the user if they really want to delete the request
    while(1):
        fetch = input("Are you sure you want to delete the request? Y/N\n")

        if fetch.upper() == 'Y':
            break #continue with deletion

        elif fetch.upper() == 'N':
            print('Request not deleted.Returning to request selection...')
            time.sleep(2)
            return

        else:
            print("Please type either 'Y' or 'N'")

    print("Deleting request...")
    time.sleep(2)

    commandString = ("DELETE FROM requests WHERE rid = '{}'").format(request[0])
    dbcursor.execute(commandString)
    database.commit()
    database.close()

    return

def viewOwnRequests(member):
    ##This function is created with the purpose of processing the member's own requests
    os.system('clear')
    #Query for the member's existing requests
    database = sqlite3.connect('testDatabase.db')
    dbcursor = database.cursor()
    queryString = ("SELECT rid, email, rdate, l1.city, l2.city, amount FROM"
                   " requests, locations l1, locations l2  WHERE email = '{}'"
                   "AND l1.lcode = pickup AND l2.lcode = dropoff").format(member)
    dbcursor.execute(queryString)
    result = dbcursor.fetchall() #fetch and store all requests in result

    if len(result) == 0:
        print("No Requests Available")
        time.sleep(2)
        return

    while len(result) != 0:
        #print out 5 results at a time
        displayedRequests = [] #will hold the requests currently displayed on the screen
        for x in range(1,6):
            if len(result) == 0:
                break

            request = result.pop()
            displayedRequests.append(request)
            print(("{}. RequestID: {}, Poster: {}, RequestDate: {}\nPickup: {}, "
                   "Dropoff: {}, Amount: {}\n").format(x, request[0], request[1], request[2], request[3], request[4], request[5]))

        #after printing out 5 requests, ask the user if they want to see more or delete a specific request
        if len(result) != 0:
            fetch = input("Type MORE to see more requests or select index of request to delete.\n"
                          "Type BACK to return to request selection screen\n")
            if fetch.upper() == 'EXIT': #IF the user wants to exit
                os.system("clear")
                print('EXITING\nThank you for using this Ride Finder')
                time.sleep(2)
                os.system('clear')
                sys.exit()

            elif fetch.upper() == 'BACK':
                os.system('clear')
                return

            elif fetch.upper() == 'MORE':
                os.system('clear')
                continue

            elif '1' <= fetch <= '5':
                #valid index. delete the request
                deleteRequest(int(fetch) - 1, displayedRequests)
                return #return to main request screen

            else: #invalid input
                print("Input invalid. Returning...")
                time.sleep(2)
                return

    #If the loop was broken, then that means all requests were printed.
    fetch = input("There are no more requests. Select index of request to delete.\n"
                  "Type BACK to return to request selection screen\n")

    if fetch.upper() == 'EXIT':  # IF the user wants to exit
        os.system("clear")
        print('EXITING\nThank you for using this Ride Finder')
        time.sleep(2)
        os.system('clear')
        sys.exit()

    elif fetch.upper() == 'BACK': #return to request selection screen
        os.system('clear')
        return

    elif '1' <= fetch <= str(len(displayedRequests)): #may not be 5 displayed requests
        # valid index. delete the request
        deleteRequest(int(fetch) - 1, displayedRequests)
        return  # return to main request selection screen

    else:  # invalid input
        print("Input invalid. Returning...\n")
        time.sleep(2)
        return


    return

def viewOtherRequests(member, dbcursor):
    ##This function is created with the purpose of viewing other member's requests
    ##The member's own requests will not appear in this list
    ##The user can enter a keyword (either location code or city)
    ##SUBSTRINGS WILL NOT BE MATCHED
    ##Only returns requests where the pickup location is in the lcode or city

    #User will specify a city or lcode
    fetch = input("Which lcode or city do you want to see pickup requests for? \n")

    if fetch.upper() == 'EXIT':  # IF the user wants to exit
        os.system("clear")
        print('EXITING\nThank you for using this Ride Finder')
        time.sleep(2)
        os.system('clear')
        sys.exit()

    elif fetch.upper() == 'BACK': #return to request selection screen
        os.system('clear')
        return

    else:
        #query the user input and return rides that match the pickup locations
        #do not include the requests of the current member
        queryString = ("SELECT rid, email, rdate, l1.city, l2.city, amount FROM"
                   " requests, locations l1, locations l2  WHERE ((l1.lcode LIKE '{}') OR (l1.city LIKE '{}'))"
                   "AND l1.lcode = pickup AND l2.lcode = dropoff AND email <> '{}'").format(fetch, fetch, member)

        dbcursor.execute(queryString)
        result = dbcursor.fetchall()

        if len(result) == 0:
            print("No Request Available")
            time.sleep(2)
            return

        while len(result) != 0:
            ##The following codeblock is similar to the codeblock
            ##found in the above function viewOwnRequests

            # print out 5 results at a time
            displayedRequests = []  # will hold the requests currently displayed on the screen
            for x in range(1, 6):
                if len(result) == 0:
                    break

                request = result.pop()
                displayedRequests.append(request)
                print(("{}. RequestID: {}, Poster: {}, RequestDate: {}\nPickup: {}, "
                       "Dropoff: {}, Amount: {}\n").format(x, request[0], request[1], request[2], request[3],
                                                           request[4], request[5]))

            # after printing out 5 requests, ask the user if they want to see more or delete a specific request
            if len(result) != 0:
                fetch = input("Type MORE to see more requests. Type index of request to message owner.\n"
                              "Type BACK to return to request selection screen\n")
                if fetch.upper() == 'EXIT':  # IF the user wants to exit
                    os.system("clear")
                    print('EXITING\nThank you for using this Ride Finder')
                    time.sleep(2)
                    os.system('clear')
                    sys.exit()

                elif fetch.upper() == 'BACK':
                    os.system('clear')
                    return

                elif fetch.upper() == 'MORE':
                    os.system('clear')
                    continue

                elif '1' <= fetch <= '5':
                    # valid index. delete the request
                    messageRequestOwner(int(fetch) - 1, displayedRequests, member)
                    return  # return to main request screen

                else:  # invalid input
                    print("Input invalid. Returning...")
                    time.sleep(2)
                    return

        # If the loop was broken, then that means all requests were printed.
        fetch = input("There are no more requests. Type index of request to message owner.\n"
                      "Type BACK to return to request selection screen\n")

        if fetch.upper() == 'EXIT':  # IF the user wants to exit
            os.system("clear")
            print('EXITING\nThank you for using this Ride Finder')
            time.sleep(2)
            os.system('clear')
            sys.exit()

        elif fetch.upper() == 'BACK':  # return to request selection screen
            os.system('clear')
            return

        elif '1' <= fetch <= str(len(displayedRequests)):  # may not be 5 displayed requests
            # valid index. message the owner
            messageRequestOwner(int(fetch) - 1, displayedRequests, member)
            return  # return to main request selection screen

        else:  # invalid input
            print("Input invalid. Returning...\n")
            time.sleep(2)
            return

        return




def searchAndDeleteRequest(dbcursor,member):
    while(1):
        os.system('clear')
        #ask the user if they want to view their own requests or search for requests
        fetch = input("Type 1 to view/delete own Requests. Type 2 to search for Requests\n")

        if fetch.upper() == 'EXIT': #IF the user wants to exit
            os.system("clear")
            print('EXITING\nThank you for using this Ride Finder')
            time.sleep(2)
            os.system('clear')
            sys.exit()

        elif fetch.upper() == 'BACK': #return user to main menu
            os.system('clear')
            return

        elif fetch == '1': #valid input
            viewOwnRequests(member)


        elif fetch == '2': #valid input
            viewOtherRequests(member, dbcursor)

        else:
            print("Invalid Input, Try Again")
            time.sleep(2)
            continue

