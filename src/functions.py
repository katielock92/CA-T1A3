# import any packages required here

import csv
import datetime
import random

class User:
    def __init__ (self, email, password):
        self.email = email
        self.password = password

def login(User):
    email = input("Please enter your email address: ")
    # check if email is in csv file
    # if email is registered, prompt for password
    # placeholder code:
    if email == "0":
        print("Welcome back!")
        password = input("Please enter your password: ")
    else:
        print("To sign up, please enter a password that is at least 10 characters in length.")
        password = input("New password: ")
        if len(password) <10:
            print("Password is too short. Please try again.")
            password = input("New password: ")
    # if email is not registered, validate the format then ask them to set a new password

def main_menu():
    display_menu = True
    while display_menu:
        print("WFDF RULES OF ULTIMATE ACCREDITATION APP - MAIN MENU")
        print("1: Begin the Rules Accreditation Quiz")
        print("2: See your previous results")
        print("3: Access the database of certified players")
        print("4: Exit application")
        menu_selection = input("Please select an option by entering the menu number: ")
        if menu_selection == "1":
            display_menu = False
            print("Option 1 selected!")
            # add quiz feature here
        elif menu_selection == "2":
            display_menu = False
            print("Option 2 selected!")
            # add previous results feature here
        elif menu_selection == "3":
            display_menu = False
            print("Option 3 selected!")
            # add certified players feature here
        elif menu_selection == "4":
            display_menu = False
            print("Option 4 selected!") 
            # add exit protocol here 
        else:
            print("Invalid menu option selected! Please try again.")
            print("Here's the menu again for you...")
            continue