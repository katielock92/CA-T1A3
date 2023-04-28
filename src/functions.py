# import any packages required here

import sys
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
users_emails = pandas.read_csv(
    './src/registered_users.csv', usecols=['user_email'])
users_ids = pandas.read_csv('./src/registered_users.csv', usecols=['user_id'])
quiz_csv = pandas.read_csv('./src/quiz_questions.csv')

# login/registration feature

def login(User):
    email = input("Please enter your email address: ")
    # need to update this to check only one column and not all
    for row in users_emails:
        if users_emails[row].str.contains(email).any():
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
            for row in users_ids:
                user_id = random.randint(1000, 50000)
                user_id = str(user_id)  # converts int to str
                # checks that user ID is unique, generates a new number if it is not
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
    
    #for i, question in enumerate(questions):
       #pass

def previous_results(User):
    pass

def certified_players (User):
    pass


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
            quiz(User)
            # add quiz feature here



        elif menu_selection == "2":
            display_menu = False
            print("Option 2 selected!")
            previous_results(User)
            # add previous results feature here



        elif menu_selection == "3":
            display_menu = False
            print("Option 3 selected!")
            certified_players(User)
            # add certified players feature here



        elif menu_selection == "4":
            display_menu = False
            print("Thank you, see you next time!")
            sys.exit(0)
        else:
            print(
                "Invalid menu option selected! Please try again.\nHere's the menu again for you...")
            continue
