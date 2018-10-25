import sys
import time
import sqlite3

def createTable(database, dbcursor, table_name, sql_statement):
    if((sql_statement[0:12]).upper() != "CREATE TABLE"):
        exit
    else:
        database_cursor = database.cursor()
        try:
            dbcursor.execute(("drop table if exists " +table_name +";"))
            dbcursor.execute("PRAGMA foreign_keys = ON;")
            dbcursor.execute(sql_statement)
            print("Successfully created table " +table_name +" in the database")
        except:
            print("Something went wrong with the format of your command, please try again.")
    database.commit()
            
()

def insertValues(database, dbcursor, table_name, sql_statement):
    if((sql_statement[0:11]).upper() != "INSERT INTO"):
        exit
    else:
        try:
            dbcursor.execute(sql_statement)
            print("Successfully inserted values into " +table_name)
        except:
            print("Something went wrong with the format of your command, please try again.")
    database.commit()
()


def main():
    exiting = False
    database = sqlite3.connect("myDatabase.db")
    dbcursor = database.cursor()

    #controlled login screen, only allows for Login and Register
    login_option = 0
    while(login_option<1 or login_option>2):
        login_option = (input("Select 1 to login as an existing user, or press 2 to register\nAt any point, type EXIT to end your session\n"))
        if not login_option[0].isdigit():
            login_option = 0
        else:
            login_option = int(login_option)

##    if login_option == 1:
##        username = input("Username:
    
    
    
    createTable(database, dbcursor, "testTable", "CREATE TABLE testTable(name CHAR(10), id int)")
    insertValues(database, dbcursor, "testTable", "INSERT INTO testTable VALUES(\"warren\", 30);")
    insertValues(database, dbcursor, "testTable", "INSERT INTO testTable VALUES(\"thomas\", 25);")
    all_rows = dbcursor.fetchall()
    print(all_rows)

    database.close()
main()
