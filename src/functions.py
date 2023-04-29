# import any packages required here:
import sys
import re
import csv
import pandas as pd
import datetime
import random

# establishing class for the user:


class User:
    def __init__(self, email, password, user_id):
        self.email = email
        self.password = password
        self.user_id = user_id

# function to check for valid email format:


def check(email):
    valid_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    email_valid = False
    while not email_valid:
        if (re.fullmatch(valid_email, email)):
            email_valid = True
            return
        else:
            print("Invalid email format, please try again.")
            email = input("Please enter your email address: ")

 

# setting up file handling, tidy this up later
registered_users_rows = ['user_email', 'user_password', 'user_id']
users_csv = pd.read_csv('./src/registered_users.csv')
users_emails = pd.read_csv(
    './src/registered_users.csv', usecols=['user_email'])
users_ids = pd.read_csv('./src/registered_users.csv', usecols=['user_id'])
quiz_csv = pd.read_csv('./src/quiz_questions.csv')


def login(User):
    email = input("Please enter your email address: ")
    for row in users_emails:
        if users_emails[row].str.contains(email).any():
            print("Welcome back!")
            password = input("Please enter your password: ")
            for index, row in users_csv.iterrows(): # validates password matches:
                if row['user_email'] == email and row['user_password'] == password:
                    print("Login successful!")
                    return
                else:
                    print("Incorrect password, please try again.")
                    password = input("Please enter your password: ")
                    continue
            
        else:
            check(email)  # checks email format is valid
            print(
                "To sign up, please set your password.\nYour password must meet the following conditions:\n- Contains at least one lower case letter\n- Contains at least one upper case letter\n- Contains 10 or more characters")

            valid_password = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{10,}$'
            password_valid = False
            while not password_valid:
                password = input("New password: ")
                # validates password against conditions in regex
                if (re.fullmatch(valid_password, password)):
                    password_valid = True
                    continue
                else:
                    print("Password does not meet required format, please try again.")

            for row in users_ids:
                user_id = random.randint(1000, 50000)
                user_id = str(user_id)  # converts int to str
                # checks that user ID is unique, generates a new number if it is not:
                if users_ids[row].astype(str).str.contains(user_id).any():
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


def quiz(User):
    print("Welcome the WFDF Rules Accreditation Quiz.\nYou can exit at time by entering '\quit'\nFor each question, please answer True or False.\nYou will see your total score at the end.")
    quiz_continue = input("Press any key to continue: ")
    print("Quiz time!")

    # revisit this later - hurting my head!

    # for i, question in enumerate(questions):
    # pass


def previous_results(User):
    # to be completed
    try:
        pass  # open and read csv file
    except:  # add except error name
        pass  # print that no previous results available


def certified_players(User):
    # to be completed
    pass


def main_menu():
    display_menu = True
    while display_menu:
        print("\nWFDF RULES OF ULTIMATE ACCREDITATION APP - MAIN MENU\n\n1: Begin the Rules Accreditation Quiz\n2: See your previous results\n3: Access the database of certified players\n4: Exit application\n")
        menu_selection = input(
            "Please select an option by entering the menu number: ")
        try:
            menu_selection = int(menu_selection)
            if menu_selection == 1:
                display_menu = False
                print("Option 1 selected!")
                quiz(User)  # calls the quiz function

            elif menu_selection == 2:
                display_menu = False
                print("Option 2 selected!")
                previous_results(User)  # calls the previous results function

            elif menu_selection == 3:
                display_menu = False
                print("Option 3 selected!")
                certified_players(User)  # calls the certified player function

            elif menu_selection == 4:
                display_menu = False
                print("Thank you, see you next time!")
                sys.exit(0)

            else:
                print(
                    "Invalid menu option selected! Please try again.\nHere's the menu again for you...")
                continue

        except ValueError:
            print(
                "That wasn't a number! Please try again.\nHere's the menu again for you...")
            continue
