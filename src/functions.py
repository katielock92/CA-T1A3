# import any packages required here

import csv
import datetime
import random


class User:
    def __init__(self, email, password, user_id):
        self.email = email
        self.password = password
        self.user_id = user_id


def login(User):
    # list of column names
    registered_users_rows = ['user_email', 'user_password', 'user_id']
    email = input("Please enter your email address: ")
    # check if email is in csv file
    # if email is registered, prompt for password
    # placeholder code:
    if email == "0":
        print("Welcome back!")
        password = input("Please enter your password: ")
        # validate password
    else:
        # if email is not registered, validate the format then ask them to set a new password
        print(
            "To sign up, please enter a password that is at least 10 characters in length.")
        password = input("New password: ")
        if len(password) < 10:
            print("Password is too short. Please try again.")
            password = input("New password: ")
        user_id = random.randint(1000, 50000)
        # check user_id is unique, otherwise run again
        login_details = {
            "user_email": email,
            "user_password": password,
            "user_id": user_id
        }
        with open('./src/registered_users.csv', 'a') as csv_file:
            dict_object = csv.DictWriter(
                csv_file, fieldnames=registered_users_rows)
            dict_object.writerow(login_details)
        print(f"\nWelcome! Your user ID is {user_id}\n")


def main_menu():
    display_menu = True
    while display_menu:
        print("\nWFDF RULES OF ULTIMATE ACCREDITATION APP - MAIN MENU\n\n1: Begin the Rules Accreditation Quiz\n2: See your previous results\n3: Access the database of certified players\n4: Exit application\n")
        menu_selection = input(
            "Please select an option by entering the menu number: ")
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
