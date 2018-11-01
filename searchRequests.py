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

def messageRequestOwner():
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

def viewOtherRequests(member):
    ##This function is created with the purpose of viewing other member's requests
    ##The member's own requests will not appear in this list
    

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
            viewOtherRequests(member)

        else:
            print("Invalid Input, Try Again")
            time.sleep(2)
            continue

