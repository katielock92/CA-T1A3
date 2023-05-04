import time

import colored
import emoji

import functions
import styles

print(colored.stylize("\nWelcome to the", styles.blue_bold))
print(emoji.emojize(colored.stylize("WFDF Rules of Ultimate :flying_disc:", styles.red_bold)))
print(colored.stylize("Accreditation Quiz App!\n", styles.blue_bold))
time.sleep(1)
print("You can use this app to test your knowledge of the rules of Ultimate and become a certified player.\n"
)
time.sleep(2)
rules_link = colored.stylize("https://rules.wfdf.org/", styles.blue_bold)
print(f"The official rules can be viewed here: {rules_link}\n")
time.sleep(2)
print("Documentation for this app can be found here: x")
print(colored.stylize("\n______________________________________________________________\n\n", styles.blue_bold))
time.sleep(2)

functions.login()
time.sleep

def main_menu():
    print(colored.stylize("\nWFDF RULES OF ULTIMATE ACCREDITATION APP - MAIN MENU\n", styles.red_bold))
    print(colored.stylize("1: Begin the Rules Accreditation Quiz", styles.blue))
    print(colored.stylize("2: See your previous results", styles.blue))
    print(colored.stylize("3: Access the database of certified players", styles.blue))
    print(colored.stylize("4: Exit application\n", styles.blue))
    menu_selection = input(colored.stylize("Please select an option by entering the menu number: ", styles.bold))
    return menu_selection

def menu_decision():
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
                print(colored.stylize(
                    "\nInvalid menu option selected! Please try again.\nHere's the menu again for you...\n", styles.red_bold)
                )
                time.sleep(1)
                continue

        except ValueError:
            print(colored.stylize(
                "\nThat wasn't a number! Please try again.\nHere's the menu again for you...\n", styles.red_bold)
            )
            time.sleep(1)
            continue

menu_decision()

print(colored.stylize("\nThank you for using the Rules Accreditation app!\n", styles.blue_bold))
