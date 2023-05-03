"""This module contains the primary feature functions for this application.

This module is designed to be used in conjunction with main.py for operation of the login feature, along with all menu features of the quiz application.
"""

import sys
import re
import csv
import datetime
import random

import pandas as pd
import colored
import emoji

import styles


class User:
    """Defines what features each unique user needs.

    Attributes:
        user_id: the unique integer User ID for this user
    """

    def __init__(self, email, password, user_id):
        """Initialises the instance for each user."""
        self.email = email
        self._password = password
        self.user_id = user_id


user = User("", "", "")


def login():
    user.email = input(
        colored.stylize("To login or register, please enter your email address: ", styles.bold)
    ).lower()
    if user.email == "\quit":
        quit()
    for row in users_emails:
        if users_emails[row].str.contains(user.email).any():
            return_login()
        else:
            check_email()
            print("To sign up, please set your password.")
            print("Your password must meet the following conditions:")
            print("- Contains at least one lower case letter")
            print("- Contains at least one upper case letter")
            print("- Contains 10 or more characters")
            check_password()
            new_user()


def quiz():
    print(colored.stylize("\nWelcome the WFDF Rules Accreditation Quiz.\n", styles.red_bold))
    print("You can exit at any time by entering '\quit'\n")
    print(
        "For each question, please answer True or False. You will see your total score at the end.\n"
    )
    prompt = input(colored.stylize("Press any key to continue: ", styles.bold)).upper()
    if prompt == "\QUIT":
        quit()
    while True:
        questions_csv = csv.reader(open("./src/quiz_questions.csv", "r"))
        quiz_dict = {}
        for row in questions_csv:
            quiz_dict[row[0]] = row[1:]
        questions = random.sample(list(quiz_dict.items()), k=20)
        user_score = 0
        for i, question in enumerate(questions):
            print(colored.stylize(f"\nQuestion {i+1}:", styles.blue_bold))
            print(colored.stylize(f"{question[0]}\n", styles.blue))
            while True:
                user_answer = input(colored.stylize("Your answer: ", styles.bold)).upper()
                if user_answer == "TRUE" or user_answer == "FALSE":
                    break
                elif user_answer == "\QUIT":
                    print(colored.stylize("\nAre you sure you want to quit? Your progress will be lost.", styles.red_bold))
                    quit_quiz = input(colored.stylize(
                        "Enter Y to proceed with exiting the application: ", styles.bold)
                    ).upper()
                    if quit_quiz == "Y":
                        quit()
                    else:
                        print(
                            "\nOK, thanks for staying. Here's the question again for you..."
                        )
                        print(colored.stylize(f"\nQuestion {i+1}:", styles.blue_bold))
                        print(colored.stylize(f"{question[0]}\n", styles.blue))
                        continue
                else:
                    print(colored.stylize("\nInvalid answer! Please enter True or False...\n", styles.red_bold))
            if user_answer in question[1]:
                user_score += 1
        attempt_date = datetime.date.today()
        expiry_date = attempt_date + datetime.timedelta(days=550)

        if user_score >= 17:
            print("Congratulations! You passed the quiz.")
            print(f"Your score was {user_score}/20")
            print(f"You are now certified until {expiry_date}")

            try:
                with open("./src/certified_players.csv"):
                    pass
                with open("./src/certified_players.csv", "a") as results:
                    write_results = csv.writer(results)
                    write_results.writerow([user.user_id, attempt_date, expiry_date])

            except FileNotFoundError as e:
                with open("./src/certified_players.csv", "a") as results:
                    write_results = csv.writer(results)
                    write_results.writerow(
                        ["User ID", "Certification Date", "Expiry Date"]
                    )
                    write_results.writerow([user.user_id, attempt_date, expiry_date])

            try:
                with open("./src/previous_results.csv"):
                    pass
                with open("./src/previous_results.csv", "a") as results:
                    write_results = csv.writer(results)
                    write_results.writerow([attempt_date, user_score, "Pass"])

            except FileNotFoundError as e:
                with open("./src/previous_results.csv", "a") as results:
                    write_results = csv.writer(results)
                    write_results.writerow(["Date", "Score", "Outcome"])
                    write_results.writerow([attempt_date, user_score, "Pass"])

        else:
            print(
                f"Your score was {user_score}/20 and a score of at least 85% is required to pass."
            )
            try:
                with open("./src/previous_results.csv"):
                    pass
                with open("./src/previous_results.csv", "a") as results:
                    write_results = csv.writer(results)
                    write_results.writerow([attempt_date, user_score, "Fail"])

            except FileNotFoundError as e:
                with open("./src/previous_results.csv", "a") as results:
                    write_results = csv.writer(results)
                    write_results.writerow(["Date", "Score", "Outcome"])
                    write_results.writerow([attempt_date, user_score, "Fail"])

                    try_again = input(
                        "Would you like to try the quiz again? Enter Y for Yes: "
                    ).upper()
                    if try_again == "Y":
                        continue
                    else:
                        break

        menu_or_quit()


def previous_results():
    try:
        with open("./src/previous_results.csv") as f:
            results = f.read()
            print(results)

    except FileNotFoundError as e:
        print("No previous results available.")

    menu_or_quit()


def certified_players():
    try:
        with open("./src/certified_players.csv") as f:
            results = f.read()
            print(results)

    except FileNotFoundError as e:
        print("No certified players on file - please contact WFDF")

    menu_or_quit()


"""When the user requests to quit, for usage in a variety of scenarios"""


def quit():
    print("Thank you for using the Rules Accreditation app!")
    sys.exit()


"""For use at the end of a feature when the input prompt is the same"""


def menu_or_quit():
    prompt = input(colored.stylize(
        'Press any key to go back to the main menu, or "\quit" to exit: ', styles.bold)
    ).lower()
    if prompt == "\quit":
        quit()




def return_login():
    print(colored.stylize("\nWelcome back!\n", styles.blue_bold))
    user._password = input(colored.stylize("Please enter your password: ", styles.bold))
    while True:
        for index, row in users_csv.iterrows():
            if user._password == "\quit":
                quit()
            if (
                row["user_email"] == user.email
                and row["user_password"] == user._password
            ):
                user.user_id = row[
                    "user_id"
                ]
                print(colored.stylize("\nLogin successful!\n", styles.blue_bold))
                return
            else:
                print(colored.stylize("\nIncorrect password, please try again.\n", styles.red_bold))
                user._password = input(colored.stylize("Please enter your password: ", styles.bold))
                continue

"""Checks that the email address of a new user is in a valid format"""

def check_email():
    valid_email = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    email_valid = False
    while not email_valid:
        if re.fullmatch(valid_email, user.email):
            email_valid = True
            return
        else:
            print(colored.stylize("\nInvalid email format, please try again.\n", styles.red_bold))
            user.email = input(colored.stylize("\nPlease enter your email address: ", styles.bold))


"""Checks that the password a new user is in a valid format"""


def check_password():
    valid_password = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{10,}$"
    password_valid = False
    while not password_valid:
        user._password = input(colored.stylize("New password: ", styles.bold))
        if re.fullmatch(valid_password, user._password):
            password_valid = True
            continue
        else:
            print(colored.stylize("Password does not meet required format, please try again.", styles.red_bold))


def new_user(users_csv):
    for row in users_ids:
        user.user_id = random.randint(1000, 50000)
        user.user_id = str(user.user_id)
        if users_ids[row].astype(str).str.contains(user.user_id).any():
            continue
        else:
            break

    login_details = {
        "user_email": user.email,
        "user_password": user._password,
        "user_id": user.user_id,
    }
    with open(users_csv, "a") as csv_file:
        registered_users_rows = ["user_email", "user_password", "user_id"]
        dict_object = csv.DictWriter(csv_file, fieldnames=registered_users_rows)
        dict_object.writerow(login_details)
        print(f"\nWelcome! Your user ID is {user.user_id}\n")


users_csv = pd.read_csv("./src/registered_users.csv")
users_emails = pd.read_csv("./src/registered_users.csv", usecols=["user_email"])
users_ids = pd.read_csv("./src/registered_users.csv", usecols=["user_id"])
