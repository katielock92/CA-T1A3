"""This module contains the feature functions for this application.

This module is designed to be used in conjunction with main.py for operation 
of the login feature, along with all menu features of the quiz application.

This app was developed for educational purposes only.

MIT License

Copyright (c) 2023 Katie Lock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
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
    """Defines what attributes each unique user needs.

    Attributes:
        user_id: the unique integer User ID for this user
    """

    def __init__(
        self, email, password, user_id, user_score, attempt_date, expiry_date, questions
    ):
        """Initialises the instance for each user."""
        self.email = email
        self._password = password
        self.user_id = user_id
        self.user_score = user_score
        self.attempt_date = attempt_date
        self.expiry_date = expiry_date
        self.questions = questions


user = User("", "", "", "", "", "", "")


class Files:
    """Defines file paths that will be frequently utilised across functions and tests.

    Attributes:
        registered_users: contains the list of registered users for the app
        certified_players: contains all players who have passed the quiz
        previous_results: contains all previous quiz attempts
    """

    def __init__(self, registered_users, certified_players, previous_results):
        """Initialises the object instance."""
        self.registered_users = registered_users
        self.certified_players = certified_players
        self.previous_results = previous_results


files = Files("registered_users.csv", "certified_players.csv", "previous_results.csv")


def welcome():
    print(colored.stylize("\nWelcome to the", styles.blue_bold))
    print(
        emoji.emojize(
            colored.stylize("WFDF Rules of Ultimate :flying_disc:", styles.red_bold)
        )
    )
    print(colored.stylize("Accreditation Quiz App!\n", styles.blue_bold))
    time.sleep(1)
    print(
        "You can use this app to test your knowledge of the rules of Ultimate and "
        "become a certified player.\n"
    )
    time.sleep(1)
    rules_link = colored.stylize("https://rules.wfdf.org/", styles.blue_bold)
    print(f"- The official rules can be viewed here: {rules_link}\n")
    time.sleep(1)
    repo_link = colored.stylize(
        "https://github.com/katielock92/CA-T1A3", styles.blue_bold
    )
    print(f"- Documentation for this app can be found here: {repo_link}")
    time.sleep(1)
    print(
        colored.stylize(
            "\nDisc in... stalling...\n\n",
            styles.blue_bold,
        )
    )
    time.sleep(1)


def login():
    user.email = input(
        colored.stylize(
            "To login or register, please enter your email address: ", styles.bold
        )
    ).lower()
    if user.email == "quit":
        quit()
    else:
        check_email(user)
    while True:
        try:
            with open(files.registered_users, "r") as f:
                reader = csv.DictReader(f)
                user_exists = False
                for row in reader:
                    if row["user_email"] == user.email:
                        user_exists = True
                        break
                if user_exists:
                    return_login()

                else:
                    print(
                        "\nTo sign up, please set your password.\n"
                        "Your password must meet the following conditions:\n"
                        "- Contains at least one lower case letter\n"
                        "- Contains at least one upper case letter\n"
                        "- Contains at least one number\n"
                        "- Contains 10 or more characters\n"
                    )
                    user._password = maskpass.askpass(prompt="New password: ", mask="*")
                    check_password()
                    new_user()
                time.sleep(2)
                return
        except FileNotFoundError:
            with open(files.registered_users, "a") as f:
                new_file = csv.writer(f)
                new_file.writerow(["user_email", "user_password", "user_id"])
                continue


def return_login():
    """For validating existing registered users"""
    print(colored.stylize("\nWelcome back!\n", styles.blue_bold))
    user._password = maskpass.askpass(prompt="Please enter your password: ", mask="*")
    while True:
        found_user = False
        for index, row in pd.read_csv(files.registered_users).iterrows():
            if user._password == "quit":
                quit()
            elif (
                row["user_email"] == user.email
                and row["user_password"] == user._password
            ):
                user.user_id = row["user_id"]
                print(colored.stylize("\nLogin successful!\n", styles.blue_bold))
                return
        if not found_user:
            print(
                emoji.emojize(
                    colored.stylize(
                        "\n:red_exclamation_mark: Incorrect password, please try again.\n",
                        styles.red_bold,
                    )
                )
            )
            user._password = maskpass.askpass(
                prompt="Please enter your password: ", mask="*"
            )
            found_user = True


def check_email(user):
    """Checks that the email address is in a valid format"""
    valid_email = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    while True:
        if re.fullmatch(valid_email, user.email):
            return
        else:
            print(
                emoji.emojize(
                    colored.stylize(
                        "\n:red_exclamation_mark: Invalid email format, please try again.\n",
                        styles.red_bold,
                    )
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
        if user._password == "quit":
                quit()
        elif re.fullmatch(valid_password, user._password):
            break
        else:
            print(
                emoji.emojize(
                    colored.stylize(
                        "\n:red_exclamation_mark: Password does not meet required format, "
                        "please try again.\n",
                        styles.red_bold,
                    )
                )
            )
            user._password = maskpass.askpass(prompt="New password: ", mask="*")
            continue


def new_user():
    """Saving the successful registration of a new user"""
    with open(files.registered_users, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            """Assigns random unique user ID"""
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
    with open(files.registered_users, "a") as f:
        registered_users_rows = ["user_email", "user_password", "user_id"]
        writer = csv.DictWriter(f, fieldnames=registered_users_rows)
        writer.writerow(login_details)
        print(f"\nWelcome! Your user ID is {user.user_id}\n")


def main_menu():
    print(
        emoji.emojize(
            colored.stylize(
                "\nWFDF RULES OF ULTIMATE ACCREDITATION APP :flying_disc:\nMAIN MENU\n",
                styles.red_bold,
            )
        )
    )
    print(
        colored.stylize(
            "1: Begin the Rules Accreditation Quiz\n"
            "2: See your previous results\n"
            "3: Access the database of certified players\n"
            "4: Exit application\n",
            styles.blue,
        )
    )


def menu_decision():
    user_decision = ""
    while user_decision != 4:
        main_menu()
        user_decision = input(
            colored.stylize(
                "Please select an option by entering the menu number: ", styles.bold
            )
        )
        try:
            user_decision = int(user_decision)
            if user_decision == 1:
                check_quiz()

            elif user_decision == 2:
                previous_results(user)
                menu_or_quit()

            elif user_decision == 3:
                certified_players()
                menu_or_quit()

            elif user_decision == 4:
                pass

            else:
                print(
                    emoji.emojize(
                        colored.stylize(
                            "\n:red_exclamation_mark: Invalid menu option selected! Please try again.\n"
                            "Here's the menu again for you...\n",
                            styles.red_bold,
                        )
                    )
                )
                time.sleep(1)
                continue

        except ValueError or TypeError:
            print(
                emoji.emojize(
                    colored.stylize(
                        "\n:red_exclamation_mark: That wasn't a number! Please try again.\n"
                        "Here's the menu again for you...\n",
                        styles.red_bold,
                    )
                )
            )
            time.sleep(1)
            continue


def check_quiz():
    """Error handling provision in case quiz questions file goes missing"""
    try:
        with open("quiz_questions.csv", "r"):
            pass
        quiz()
    except FileNotFoundError:
        print(
            emoji.emojize(
                colored.stylize(
                    "\n:red_exclamation_mark: Error! Quiz questions missing.\n"
                    "Please contact app creator to rectify.",
                    styles.red_bold,
                )
            )
        )
        print(colored.stylize("\nReturning to the main menu...\n", styles.blue_bold))
        time.sleep(1.5)
        return


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
        user.attempt_date = datetime.date.today()

        if user.user_score >= 17:
            pass_quiz(user)
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
                    colored.stylize(
                        "\nReturning to the main menu...\n", styles.blue_bold
                    )
                )
                time.sleep(1.5)
                return
    menu_or_quit()


def new_quiz(user):
    """Inner loop for each unique quiz instance"""
    questions_csv = csv.reader(open("quiz_questions.csv", "r"))
    quiz_dict = {}
    for row in questions_csv:
        quiz_dict[row[0]] = row[1:]
    user.questions = random.sample(list(quiz_dict.items()), k=20)
    run_quiz(user)


def run_quiz(user):
    user.user_score = 0
    for i, question in enumerate(user.questions):
        print(colored.stylize(f"\nQuestion {i+1}:", styles.blue_bold))
        print(colored.stylize(f"{question[0]}\n", styles.blue))
        while True:
            user_answer = input(colored.stylize("Your answer: ", styles.bold)).upper()
            if user_answer == "TRUE" or user_answer == "FALSE":
                break
            elif user_answer == "QUIT":
                print(
                    emoji.emojize(
                        colored.stylize(
                            "\n:red_exclamation_mark: Are you sure you want to quit? "
                            "Your progress will be lost.",
                            styles.red_bold,
                        )
                    )
                )
                quit_quiz = input(
                    colored.stylize(
                        "\nEnter Y to proceed with exiting the application: ",
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
                    emoji.emojize(
                        colored.stylize(
                            "\n:red_exclamation_mark: Invalid answer! Please enter True or False...\n",
                            styles.red_bold,
                        )
                    )
                )
        if user_answer in question[1]:
            user.user_score += 1


def pass_quiz_text(user):
    print(
        emoji.emojize(
            colored.stylize(
                "\n:party_popper: Congratulations! You passed the quiz.\n",
                styles.blue_bold,
            )
        )
    )
    print(
        colored.stylize(
            f"Your score was {user.user_score}/20\n"
            f"You are now certified until {user.expiry_date}\n",
            styles.bold,
        )
    )


def pass_quiz_certified(user, files):
    try:
        with open(files.certified_players, "r"):
            pass
        with open(files.certified_players, "a") as results:
            write_results = csv.writer(results)
            write_results.writerow([user.user_id, user.attempt_date, user.expiry_date])

    except FileNotFoundError:
        with open(files.certified_players, "a") as results:
            write_results = csv.writer(results)
            write_results.writerow(["User ID", "Certification Date", "Expiry Date"])
            write_results.writerow([user.user_id, user.attempt_date, user.expiry_date])


def pass_quiz_results(user, files):
    try:
        with open(files.previous_results, "r"):
            pass
        with open(files.previous_results, "a") as results:
            write_results = csv.writer(results)
            write_results.writerow(
                [user.user_id, user.attempt_date, user.user_score, "Pass"]
            )

    except FileNotFoundError:
        with open(files.previous_results, "a") as results:
            write_results = csv.writer(results)
            write_results.writerow(["User ID", "Date", "Score", "Outcome"])
            write_results.writerow(
                [user.user_id, user.attempt_date, user.user_score, "Pass"]
            )


def pass_quiz(user):
    """Executes when the user passes the quiz"""
    user.expiry_date = user.attempt_date + datetime.timedelta(days=550)
    pass_quiz_text(user)
    pass_quiz_certified(user, files)
    pass_quiz_results(user, files)


def fail_quiz_text(user):
    print(
        emoji.emojize(
            colored.stylize(
                "\n:disappointed_face: Sorry, you didn't pass this time.",
                styles.blue_bold,
            )
        )
    )
    print(
        colored.stylize(
            f"\nYour score was {user.user_score}/20 and a score of at least "
            "85% is required to pass.\n",
            styles.bold,
        )
    )


def fail_quiz_results(user, files):
    try:
        with open(files.previous_results, "a") as results:
            write_results = csv.writer(results)
            write_results.writerow(
                [user.user_id, user.attempt_date, user.user_score, "Fail"]
            )

    except FileNotFoundError:
        with open(files.previous_results, "a") as results:
            write_results = csv.writer(results)
            write_results.writerow(["User ID", "Date", "Score", "Outcome"])
            write_results.writerow(
                [user.user_id, user.attempt_date, user.user_score, "Fail"]
            )


def fail_quiz(user):
    """Executes when the user fails the quiz"""
    fail_quiz_text(user)
    fail_quiz_results(user, files)


def previous_results(user):
    matching_results = []
    while True:
        try:
            with open(files.previous_results) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if str(user.user_id) in row["User ID"]:
                        matching_results.append(row)
                if len(matching_results) > 0:
                    print("\n")
                    for row in matching_results:
                        print(row)
                    print("\n")
                    return
                else:
                    print(
                        colored.stylize(
                            "\nNo previous results available.\n", styles.red_bold
                        )
                    )
                    return

        except FileNotFoundError:
            with open(files.previous_results, "a") as f:
                new_file = csv.writer(f)
                new_file.writerow(["User ID", "Date", "Score", "Outcome"])
                continue


def certified_players():
    try:
        with open(files.certified_players) as file:
            results = file.read()
            print(f"\n{results}\n")

    except FileNotFoundError:
        print(
            emoji.emojize(
                colored.stylize(
                    "\n:red_exclamation_mark: No certified players on file - please contact WFDF\n",
                    styles.red_bold,
                )
            )
        )


def quit():
    """When the user requests to quit, for usage in a variety of scenarios"""
    print(
        emoji.emojize(
            colored.stylize(
                "\n:waving_hand: Thank you for using the Rules Accreditation app!\n",
                styles.blue_bold,
            )
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
    else:
        print(colored.stylize("\nReturning to the main menu...\n", styles.blue_bold))
        time.sleep(1.5)
        return
