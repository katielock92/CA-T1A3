# import any packages required here:
import re
import csv
import pandas as pd
from datetime import date, timedelta
import random
import colored
import emoji


# TODO setting up file handling, tidy this up later

users_csv = pd.read_csv("./src/registered_users.csv")
users_emails = pd.read_csv("./src/registered_users.csv", usecols=["user_email"])
users_ids = pd.read_csv("./src/registered_users.csv", usecols=["user_id"])

# establishing class for the user:


class User:
    def __init__(self, email, password, user_id):
        self.email = email
        self.__password = password
        self.user_id = user_id


user = User("", "", "")

# function to check for valid email format:


def check_email():
    valid_email = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    email_valid = False
    while not email_valid:
        if re.fullmatch(valid_email, user.email):
            email_valid = True
            return
        else:
            print("Invalid email format, please try again.")
            user.email = input("Please enter your email address: ")


def check_password():
    valid_password = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{10,}$"
    password_valid = False
    while not password_valid:
        user.__password = input("New password: ")
        # validates password against conditions in regex
        if re.fullmatch(valid_password, user.__password):
            password_valid = True
            continue
        else:
            print("Password does not meet required format, please try again.")


def login():
    user.email = input("To login or register, please enter your email address: ")
    for row in users_emails:
        if users_emails[row].str.contains(user.email).any():
            print("Welcome back!")
            user.__password = input("Please enter your password: ")
            for index, row in users_csv.iterrows():  # validates password matches:
                if (
                    row["user_email"] == user.email
                    and row["user_password"] == user.__password
                ):
                    user.user_id = row["user_id"] # obtains user ID from file and sets variable
                    print("Login successful!")
                    return
                else:
                    print("Incorrect password, please try again.")
                    user.__password = input("Please enter your password: ")
                    continue

        else:
            check_email()  # checks email format is valid
            print("To sign up, please set your password.")
            print("Your password must meet the following conditions:")
            print("- Contains at least one lower case letter")
            print("- Contains at least one upper case letter")
            print("- Contains 10 or more characters")
            check_password()  # asks user to set new password, checks is valid

            for row in users_ids:
                user.user_id = random.randint(1000, 50000)
                user.user_id = str(user.user_id)  # converts int to str
                # checks that user ID is unique, generates a new number if it is not:
                if users_ids[row].astype(str).str.contains(user.user_id).any():
                    continue
                else:
                    break
            login_details = {
                "user_email": user.email,
                "user_password": user.__password,
                "user_id": user.user_id,
            }
            with open(
                "./src/registered_users.csv", "a"
            ) as csv_file:  # adds new user to file
                registered_users_rows = ["user_email", "user_password", "user_id"]
                dict_object = csv.DictWriter(csv_file, fieldnames=registered_users_rows)
                dict_object.writerow(login_details)
            print(f"\nWelcome! Your user ID is {user.user_id}\n")
            break


def quiz():
    print("Welcome the WFDF Rules Accreditation Quiz.")
    print("You can exit at time by entering '\quit'")
    print(
        "For each question, please answer True or False. You will see your total score at the end."
    )
    continue_prompt = input("Press any key to continue: ")

    while True:
        questions_csv = csv.reader(open("./src/quiz_questions.csv", "r"))
        quiz_dict = {}
        for row in questions_csv:
            quiz_dict[row[0]] = row[1:]
        questions = random.sample(list(quiz_dict.items()), k=20)
        user_score = 0
        for i, question in enumerate(questions):
            print(f"Question {i+1}: {question[0]}")
            while True:
                user_answer = input("Your answer: ").upper()
                if user_answer == "TRUE" or user_answer == "FALSE":
                    break
                else:
                    print("Invalid answer! Please enter True or False")
            if user_answer in question[1]:
                user_score = user_score + 1
        attempt_date = date.today()
        expiry_date = attempt_date + timedelta(days=550)

        if user_score >= 17:
            print("Congratulations! You passed the quiz.")
            print(f"Your score was {user_score}/20")

            # write results to certified players file"

            try:
                with open("./src/certified_players.csv"):
                    pass
                with open("./src/certified_players.csv", "a") as results:
                    write_results = csv.writer(results)
                    write_results.writerow([user.user_id, attempt_date, expiry_date])
                    # TODO get user_id working from login

            except FileNotFoundError as e:
                with open("./src/certified_players.csv", "a") as results:
                    write_results = csv.writer(results)
                    write_results.writerow(["Date", "Score", "Outcome"])
                    write_results.writerow([user.user_id, attempt_date, expiry_date])

            # write score to previous results file:
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

            break
        else:
            print(
                f"Your score was {user_score}/20 and a score of at least 85% is required to pass."
            )
            # write score to previous results file:
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

    return_prompt = input("Press any key to go back to the main menu: ")


def previous_results():
    try:
        with open("./src/previous_results.csv") as f:
            results = f.read()
            print(results)

    except FileNotFoundError as e:
        print("No previous results available.")

    return_prompt = input("Press any key to return to the main menu: ")


def certified_players():
    try:
        with open("./src/certified_players.csv") as f:
            results = f.read()
            print(results)

    except FileNotFoundError as e:
        print("No certified players on file - please contact WFDF")

    return_prompt = input("Press any key to return to the main menu: ")
