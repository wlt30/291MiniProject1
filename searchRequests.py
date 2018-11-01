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

def viewOwnRequests(dbcursor):
    ##This function is created with the purpose of processing the member's own requests

    return

def viewOtherRequests(dbcursor):
    ##This function is created with the purpose of viewing other member's requests
    ##The member's own requests will not appear in this list
    return

def searchAndDeleteRequest(dbcursor):
    while(1):
        os.system('clear')
        #ask the user if they want to view their own requests or search for requests
        fetch = input("Type 1 to view own Requests. Type 2 to search for Requests\n")

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
            viewOwnRequests(dbcursor)

        elif fetch == '2': #valid input
            viewOtherRequests(dbcursor)

        else:
            print("Invalid Input, Try Again")
            time.sleep(2)
            continue

