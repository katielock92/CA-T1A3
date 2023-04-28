# import any packages required here

import csv
import pandas
import datetime
import random

# establishing class for the user


class User:
    def __init__(self, email, password, user_id):
        self.email = email
        self.password = password
        self.user_id = user_id


# setting up file handling
registered_users_rows = ['user_email', 'user_password', 'user_id']
users_csv = pandas.read_csv('./src/registered_users.csv')

# login/registration feature

def login(User):
    email = input("Please enter your email address: ")
    # need to update this to check only one column and not all
    for col in users_csv:
        if users_csv[col].str.contains(email).any():
            print("Welcome back!")
            password = input("Please enter your password: ")
            # need to add code to validate password
            break
        else:
            # need to add code to validate email is in correct format
            print(
                "To sign up, please enter a password that is at least 10 characters in length.")
            # setting new password:
            password = "temp"
            while len(password) < 10:
                password = input("New password: ")
                if len(password) < 10:
                    print("Password is too short. Please try again.")
                    continue
                else:
                    break
            for col in users_csv:
                user_id = random.randint(1000, 50000)
                user_id = str(user_id)  # converts int to str
                if users_csv[col].str.contains(user_id).any():  # checks that user ID is unique, generates a new number if it is not
                    continue
                else:
                    break
            login_details = {
                "user_email": email,
                "user_password": password,
                "user_id": user_id
            }
            with open('./src/registered_users.csv', 'a') as csv_file:  # adds new user to file
                dict_object = csv.DictWriter(
                    csv_file, fieldnames=registered_users_rows)
                dict_object.writerow(login_details)
            print(f"\nWelcome! Your user ID is {user_id}\n")
            break

# main menu feature (other feature embedded within)


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
