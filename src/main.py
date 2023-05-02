import functions

# WELCOME SCREEN:
print("Welcome to the WFDF Rules of Ultimate Accreditation Quiz App!")
print(
    "You can use this app to test your knowledge of the rules of Ultimate and become a certified player."
)
print("The official rules can be viewed here: https://rules.wfdf.org/")

functions.login()

# DEFINING MAIN MENU:


def main_menu():
    print("WFDF RULES OF ULTIMATE ACCREDITATION APP - MAIN MENU\n")
    print("1: Begin the Rules Accreditation Quiz")
    print("2: See your previous results")
    print("3: Access the database of certified players")
    print("4: Exit application\n")
    menu_selection = input("Please select an option by entering the menu number: ")
    return menu_selection


# MAIN MENU:

user_decision = ""

while user_decision != 4:
    user_decision = main_menu()
    try:
        user_decision = int(user_decision)
        if user_decision == 1:
            functions.quiz()

        elif user_decision == 2:
            functions.previous_results()

        elif user_decision == 3:
            functions.certified_players()

        elif user_decision == 4:
            pass

        else:
            print(
                "Invalid menu option selected! Please try again.\nHere's the menu again for you..."
            )
            continue

    except ValueError:
        print(
            "That wasn't a number! Please try again.\nHere's the menu again for you..."
        )
        continue


print("Thank you for using the Rules Accreditation app!")
