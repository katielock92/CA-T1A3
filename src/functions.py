"""This module contains the primary feature functions for this application.

This module is designed to be used in conjunction with main.py for operation of the login feature, along with all menu features of the quiz application.
"""

import sys
import re
import csv
import datetime
import random
import time

import pandas as pd
import colored
import emoji
import maskpass

import styles


class User:
    """Defines what features each unique user needs.

    Attributes:
        user_id: the unique integer User ID for this user
    """

    def __init__(self, email, password, user_id, user_score):
        """Initialises the instance for each user."""
        self.email = email
        self._password = password
        self.user_id = user_id
        self.user_score = user_score


user = User("", "", "", "")


def login():
    user.email = input(
        colored.stylize(
            "To login or register, please enter your email address: ", styles.bold
        )
    ).lower()
    check_email()
    if user.email == "quit":
        quit()
    while True:
        try:
            with open("./src/registered_users.csv", "r") as f:
                reader = csv.DictReader(f)
                user_exists = False
                for row in reader:
                    if row["user_email"] == user.email:
                        user_exists = True
                        break
                if user_exists:
                    return_login()

                else:
                    print("\nTo sign up, please set your password.")
                    print("Your password must meet the following conditions:")
                    print("- Contains at least one lower case letter")
                    print("- Contains at least one upper case letter")
                    print("- Contains 10 or more characters\n")
                    check_password()
                    new_user()
                time.sleep(2)
                return
        except FileNotFoundError:
            with open("./src/registered_users.csv", "a") as f:
                new_file = csv.writer(f)
                new_file.writerow(["user_email", "user_password", "user_id"])
                continue


def return_login():
    """For validating existing registered users"""
    print(colored.stylize("\nWelcome back!\n", styles.blue_bold))
    user._password = maskpass.askpass(prompt="Please enter your password: ", mask="#")
    while True:
        found_user = False
        for index, row in pd.read_csv("./src/registered_users.csv").iterrows():
            if user._password == "quit":
                quit()
            if (
                row["user_email"] == user.email
                and row["user_password"] == user._password
            ):
                user.user_id = row["user_id"]
                print(colored.stylize("\nLogin successful!\n", styles.blue_bold))
                print(f"Your user ID is {user.user_id}")
                return
        if not found_user:
            print(
                colored.stylize(
                    "\nIncorrect password, please try again.\n", styles.red_bold
                )
            )
            user._password = maskpass.askpass(
                prompt="Please enter your password: ", mask="#"
            )
            found_user = True


def check_email():
    """Checks that the email address is in a valid format"""
    valid_email = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    while True:
        if re.fullmatch(valid_email, user.email):
            return
        else:
            print(
                colored.stylize(
                    "\nInvalid email format, please try again.\n", styles.red_bold
                )
            )
            user.email = input(
                colored.stylize("Please enter your email address: ", styles.bold)
            )
            continue


def check_password():
    """Checks that the password a new user is in a valid format"""
    valid_password = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{10,}$"
    while True:
        user._password = maskpass.askpass(prompt="New password: ", mask="#")
        if re.fullmatch(valid_password, user._password):
            return
        else:
            print(
                colored.stylize(
                    "\nPassword does not meet required format, please try again.\n",
                    styles.red_bold,
                )
            )
            continue


def new_user():
    """Saving the successful registration of a new user"""
    users_csv = "./src/registered_users.csv"
    with open(users_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            user.user_id = random.randint(1000, 50000)
            user.user_id = str(user.user_id)
            if row["user_id"] == user.user_id:
                continue
            else:
                break

    login_details = {
        "user_email": user.email,
        "user_password": user._password,
        "user_id": user.user_id,
    }
    with open("./src/registered_users.csv", "a") as f:
        registered_users_rows = ["user_email", "user_password", "user_id"]
        writer = csv.DictWriter(f, fieldnames=registered_users_rows)
        writer.writerow(login_details)
        print(f"\nWelcome! Your user ID is {user.user_id}\n")


def quiz():
    """Outer loop for the quiz feature"""
    print(
        emoji.emojize(
            colored.stylize(
                "\n\nWelcome the WFDF Rules Accreditation Quiz :flying_disc:\n",
                styles.red_bold,
            )
        )
    )
    time.sleep(1)
    print('You can exit at any time by entering "quit"\n')
    time.sleep(1)
    print(
        "For each question, please answer True or False. You will see your total score at the end.\n"
    )
    time.sleep(1)
    prompt = input(colored.stylize("Press any key to continue: ", styles.bold)).upper()
    if prompt == "QUIT":
        quit()
    while True:
        new_quiz(user)
        if user.user_score >= 17:
            pass_quiz(user)
            print(colored.stylize("\nReturning the main menu...\n", styles.blue_bold))
            time.sleep(1.5)
            break

        else:
            fail_quiz(user)
            try_again = input(
                "Would you like to try the quiz again? Enter Y for Yes: "
            ).upper()
            if try_again == "Y":
                continue
            else:
                print(
                    colored.stylize("\nReturning the main menu...\n", styles.blue_bold)
                )
                time.sleep(1.5)
                return

    menu_or_quit()


def new_quiz(user):
    """Inner loop for each unique quiz instance"""
    questions_csv = csv.reader(open("./src/quiz_questions.csv", "r"))
    quiz_dict = {}
    for row in questions_csv:
        quiz_dict[row[0]] = row[1:]
    questions = random.sample(list(quiz_dict.items()), k=20)
    user.user_score = 0
    for i, question in enumerate(questions):
        print(colored.stylize(f"\nQuestion {i+1}:", styles.blue_bold))
        print(colored.stylize(f"{question[0]}\n", styles.blue))
        while True:
            user_answer = input(colored.stylize("Your answer: ", styles.bold)).upper()
            if user_answer == "TRUE" or user_answer == "FALSE":
                break
            elif user_answer == "QUIT":
                print(
                    colored.stylize(
                        "\nAre you sure you want to quit? Your progress will be lost.",
                        styles.red_bold,
                    )
                )
                quit_quiz = input(
                    colored.stylize(
                        "Enter Y to proceed with exiting the application: ",
                        styles.bold,
                    )
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
                print(
                    colored.stylize(
                        "\nInvalid answer! Please enter True or False...\n",
                        styles.red_bold,
                    )
                )
        if user_answer in question[1]:
            user.user_score += 1


def pass_quiz(user):
    """Executes when the user passes the quiz"""
    attempt_date = datetime.date.today()
    expiry_date = attempt_date + datetime.timedelta(days=550)
    print(
        colored.stylize("\nCongratulations! You passed the quiz.\n", styles.blue_bold)
    )
    print(f"Your score was {user.user_score}/20")
    print(f"You are now certified until {expiry_date}")

    try:
        with open("./src/certified_players.csv"):
            pass
        with open("./src/certified_players.csv", "a") as results:
            write_results = csv.writer(results)
            write_results.writerow([user.user_id, attempt_date, expiry_date])

    except FileNotFoundError:
        with open("./src/certified_players.csv", "a") as results:
            write_results = csv.writer(results)
            write_results.writerow(["User ID", "Certification Date", "Expiry Date"])
            write_results.writerow([user.user_id, attempt_date, expiry_date])

    try:
        with open("./src/previous_results.csv"):
            pass
        with open("./src/previous_results.csv", "a") as results:
            write_results = csv.writer(results)
            write_results.writerow(
                [user.user_id, attempt_date, user.user_score, "Pass"]
            )

    except FileNotFoundError:
        with open("./src/previous_results.csv", "a") as results:
            write_results = csv.writer(results)
            write_results.writerow(["User ID", "Date", "Score", "Outcome"])
            write_results.writerow(
                [user.user_id, attempt_date, user.user_score, "Pass"]
            )


def fail_quiz(user):
    """Executes when the user fails the quiz"""
    attempt_date = datetime.date.today()
    print(
        f"Your score was {user.user_score}/20 and a score of at least 85% is required to pass."
    )
    try:
        with open("./src/previous_results.csv"):
            pass
        with open("./src/previous_results.csv", "a") as results:
            write_results = csv.writer(results)
            write_results.writerow(
                [user.user_id, attempt_date, user.user_score, "Fail"]
            )

    except FileNotFoundError:
        with open("./src/previous_results.csv", "a") as results:
            write_results = csv.writer(results)
            write_results.writerow(["User ID", "Date", "Score", "Outcome"])
            write_results.writerow(
                [user.user_id, attempt_date, user.user_score, "Fail"]
            )


def previous_results(user):
    matching_results = []
    while True:
        try:
            with open("./src/previous_results.csv") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if str(user.user_id) in row["User ID"]:
                        matching_results.append(row)
                if len(matching_results) > 0:
                    for row in matching_results:
                        print(row)
                    return
                else:
                    print(
                        colored.stylize(
                            "\nNo previous results available.\n", styles.red_bold
                        )
                    )
                    return

        except FileNotFoundError:
            with open("./src/previous_results.csv", "a") as f:
                new_file = csv.writer(f)
                new_file.writerow(["User ID", "Date", "Score", "Outcome"])
                continue


def certified_players(user):
    try:
        with open("./src/certified_players.csv") as f:
            results = f.read()
            print(results)

    except FileNotFoundError:
        print(
            colored.stylize(
                "\nNo certified players on file - please contact WFDF\n",
                styles.red_bold,
            )
        )


def quit():
    """When the user requests to quit, for usage in a variety of scenarios"""
    print(
        colored.stylize(
            "\nThank you for using the Rules Accreditation app!\n", styles.blue_bold
        )
    )
    sys.exit()


def menu_or_quit():
    """For use at the end of a feature when the input prompt is the same"""
    prompt = input(
        colored.stylize(
            'Press any key to go back to the main menu, or "quit" to exit: ',
            styles.bold,
        )
    ).lower()
    if prompt == "quit":
        quit()
