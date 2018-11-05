import sys
import time
import sqlite3
import getpass
import os
import datetime
import platform

if((platform.system()) == "Windows"):
    cls = 'cls'
elif((platform.system()) == "Linux"):
    cls = 'clear'
elif((platform.system()) == "Darwin"):
    cls = 'clear'

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
                                                                                                
    validSrc = False
    while not validSrc:
        stop = input("Enter a source location (max 16 characters): ")
        if len(stop) >16:
            print("Invalid input format, please try again ")
            continue
        
        dbcursor.execute("SELECT * FROM locations  WHERE lcode LIKE \"%"+stop+"%\"  OR city LIKE \"%"+stop+"%\" OR prov LIKE \"%"+stop+"%\" OR address LIKE \"%"+stop+"%\"")
        srcOptions = dbcursor.fetchall()
        if len(srcOptions) == 0:
            print("Sorry, we couldn't find any lcode, city, prov or address with that tag")
            time.sleep(0.5)
            os.system(cls)
            continue
        elif len(srcOptions) ==1:
            src = srcOptions[0][0]
            validSrc = True
            break
            

        while len(srcOptions) != 0:
            displayedOptions = []
            print("Returning Search Results \n")
            for x in range(0,5):
                if len(srcOptions) ==0:
                    break
                option = srcOptions.pop()
                displayedOptions.append(option)
                print(str(x+1) +". " +str(option))

            if len(srcOptions) != 0:
                fetch = input("There Are More Results. Press ENTER to see more results, EXIT to exit the program, or type the option number to select the location\n")

                if fetch.upper() == '':
                    os.system(cls) 
                    continue

                elif '1' <= fetch <= '5':
                    #the user wants to choose that option
                    src = displayedOptions[int(fetch)-1][0]
                    validSrc = True
                    break

                elif fetch.upper() == 'EXIT':
                    exitApp()

                else:
                    os.system(cls)
                    print("invalid input\n")
                    time.sleep(2)
                    os.system(cls)
                    break
            else:
                fetch = input("Please select an option: ")
##                if fetch.upper() == '':
##                    os.system(cls) 
##                    continue
                if '1' <= fetch <= str(x):
                    #the user wants to choose that option
                    src = displayedOptions[int(fetch)-1][0]
                    validSrc = True
                    break
                elif fetch.upper() == 'EXIT':
                    exitApp()

                else:
                    os.system(cls)
                    print("invalid input\n")
                    time.sleep(2)
                    os.system(cls)
                    break
                

        if len(srcOptions) != 0: #this case occurs if the user returned before seeing all the rides. in this case return to beginning
            continue
    
    validDst = False
    while not validDst:
        stop = input("Enter a destination location (max 16 characters): ")
        if len(stop) >16:
            print("Invalid input format, please try again ")
            continue
        
        dbcursor.execute("SELECT * FROM locations  WHERE lcode LIKE \"%"+stop+"%\"  OR city LIKE \"%"+stop+"%\" OR prov LIKE \"%"+stop+"%\" OR address LIKE \"%"+stop+"%\"")
        dstOptions = dbcursor.fetchall()
        if len(dstOptions) == 0:
            print("Sorry, we couldn't find any lcode, city, prov or address with that tag")
            time.sleep(0.5)
            os.system(cls)
            continue
        elif len(dstOptions) ==1:
            dst = dstOptions[0][0]
            validDst = True
            break

        while len(dstOptions) != 0:
            displayedOptions = []
            print("Returning Search Results \n")
            for x in range(0,5):
                if len(dstOptions) == 0:
                    break
                option = dstOptions.pop()
                displayedOptions.append(option)
                print(str(x+1) +". " +str(option))

            if len(dstOptions) != 0:
                fetch = input("There Are More Results. Press ENTER to see more results, EXIT to exit the program, or type the option number to select the location\n")

                if fetch.upper() == '':
                    os.system(cls)
                    continue

                elif '1' <= fetch <= '5':
                    #the user wants to choose that option
                    dst = displayedOptions[int(fetch)-1][0]
                    validDst = True
                    break

                elif fetch.upper() == 'EXIT':
                    exitApp()

                else:
                    os.system(cls)
                    print("invalid input\n")
                    time.sleep(2)
                    os.system(cls)
                    break
            else:
                fetch = input("Please select an option")
##                if fetch.upper() == '':
##                    os.system(cls) 
##                    continue
                if '1' <= fetch <= str(x):
                    #the user wants to choose that option
                    dst = displayedOptions[int(fetch)-1][0]
                    validDst = True
                    break
                elif fetch.upper() == 'EXIT':
                    exitApp()

                else:
                    os.system(cls)
                    print("invalid input\n")
                    time.sleep(2)
                    os.system(cls)
                    break
                

        if len(dstOptions) != 0: #this case occurs if the user returned before seeing all the rides. in this case return to beginning
            continue



    validEnroutes = False
    enroutes = []
    while not validEnroutes:
        chosen = False
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
        if len(stopOptions) == 0:
            print("Sorry, we couldn't find any lcode, city, prov or address with that tag")
            time.sleep(0.5)
            os.system(cls)
            continue
        elif len(stopOptions) ==1:
            enroutes.append(stopOptions[0][0])
            chosen = True
            continue

        while len(stopOptions) != 0 and not chosen:
            displayedOptions = []
            print("Returning Search Results \n")
            for x in range(0,5):
                if len(stopOptions) ==0:
                    break
                option = stopOptions.pop()
                displayedOptions.append(option)
                print(str(x+1) +". " +str(option))

            if len(stopOptions) != 0:
                fetch = input("There Are More Results. Press ENTER to see more results, EXIT to exit the program, or type the option number to select the location\n")

                if fetch.upper() == '':
                    os.system(cls) 
                    continue

                elif '1' <= fetch <= '5':
                    #the user wants to choose that option
                    enroutes.append(displayedOptions[int(fetch)-1][0])
                    chosen = True
                    break

                elif fetch.upper() == 'EXIT':
                    exitApp()

                else:
                    os.system(cls)
                    print("invalid input\n")
                    time.sleep(2)
                    os.system(cls)
                    break
            else:
                fetch = input("Please select an option")
                if fetch.upper() == '':
                    os.system(cls) 
                    continue
                if '1' <= fetch <= str(x):
                    #the user wants to choose that option
                    enroutes.append(displayedOptions[int(fetch)-1][0])
                    break
                elif fetch.upper() == 'EXIT':
                    exitApp()

                else:
                    os.system(cls)
                    print("invalid input\n")
                    time.sleep(2)
                    os.system(cls)
                    break
                

        if len(stopOptions) != 0: #this case occurs if the user returned before seeing all the rides. in this case return to beginning
            continue
        

    while not validCar:
        cno = input("Please enter a car number or press ENTER to skip: ")
        if cno.isdigit():
            #prevents SQL injection because car_no cannot be "cno" and still get into this SQL call
            dbcursor.execute("SELECT cno, make, model, year, seats FROM cars WHERE cno = "+cno+" AND owner = \""+member+"\"")
            cars = dbcursor.fetchone()
            if len(cars)==0:
                print("That car was not found or does not belong to you, please try again")
                continue
            else:
                validCar = True
                print(cars)
        elif cno == "":
            validCar= True
            # only way to get out of loop
            cno = None
        else:
            print("Something went wrong, please try again")
            continue

    dbcursor.execute("INSERT INTO rides VALUES (\""+rno+"\", \""+pricePerSeat+"\", \""+date+"\", \""+noSeats+"\", \""+lugDesc+"\", \""+str(src)+"\", \""+str(dst)+"\", \""+driver+"\", ?)", (cno,))
    for item in enroutes:
        dbcursor.execute("INSERT INTO enroute VALUES (\"" +rno+"\", \""+item[0]+"\")")
    os.system(cls)
