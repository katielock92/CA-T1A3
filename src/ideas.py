"""This is my code dumping ground - to be deleted"""


# test idea
def test_menu_selection(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: next("option"))
    with pytest.raises(ValueError):
        main.menu_decision()



def test_previous_results():
    with open(test_results, "w") as f:
        f.write("result1, result2, result3")

    with patch.object(
        builtins, "open", MagicMock(return_value=open(test_results, "r"))
    ):
        with patch("builtins.print") as mock_print:
            functions.previous_results()

            mock_print.assert_called_with("result1,result2,result3")

    import os

    os.remove(test_results)


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

@pytest.fixture
def sample_data():
    user.email = "x"
    user._password = "x"


def test_invalid_email(sample_data):
    functions.check_email()

def test_valid_password():
    with patch("builtins.input", return_value="MyPassword1$") as mock_input:
        functions.check_password()


def test_check_password_invalid():
    with patch("builtins.input", return_value="mypassword") as mock_input:
        with pytest.raises(SystemExit):
            functions.check_password()




import datetime
import csv
from unittest.mock import patch, mock_open
from my_module import fail_quiz

def test_fail_quiz(monkeypatch):
    user = MockUser(user_score=16) # Replace with your own implementation of a mock user object
    attempt_date = datetime.date.today()
    expected_output = f"Your score was {user.user_score}/20 and a score of at least 85% is required to pass."

    with patch('builtins.open', mock_open()) as mock_file:
        # Call the function
        fail_quiz(user)

        # Assert the output message
        assert expected_output in mock_file().write.call_args[0][0]

        # Assert that the results were written to the CSV file
        write_results = csv.writer(mock_file().write.mock_calls[0][1][0])
        assert write_results.writerow.call_args_list == [
            call(["Date", "Score", "Outcome"]),
            call([attempt_date, user.user_score, "Fail"])
        ]



"""Test X: New Quiz"""


@pytest.fixture
def questions_csv():
    # Sample CSV data to test the function with
    return StringIO(
        "question1,True\nquestion2,True\nquestion3,True\nquestion4,True\nquestion5,True\nquestion6,True\nquestion7,True\nquestion8,True\nquestion9,True\nquestion10,True\nquestion11,True\nquestion12,True\nquestion13,True\nquestion14,True\nquestion15,True\nquestion16,True\nquestion17,True\nquestion18,True\nquestion19,True\nquestion20,True"
    )


def test_new_quiz(questions_csv, monkeypatch):
    user = MockUser("", "", "", "")
    # Mock the csv file with a StringIO object for testing purposes
    monkeypatch.setattr("builtins.open", lambda file, mode: questions_csv)

    # Mock the csv reader object to return the sample questions
    csv_reader = csv.reader(questions_csv)
    monkeypatch.setattr("csv.reader", lambda *args: csv_reader)

    # Mock the input function to test different inputs

    inputs = iter(
        [
            "True",
            "true",
            "True",
            "true",
            "True",
            "true",
            "True",
            "true",
            "True",
            "true",
            "True",
            "true",
            "True",
            "false",
            "false",
            "false",
            "false",
            "false",
            "false",
            "false",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    # Call the function and check the user score
    functions.new_quiz(user)
    assert user.user_score == 13

