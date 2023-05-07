"""This module contains the unit tests for this application.

To run the tests, the application will need to be available through your
machine and Pytest will need to be installed.  This will automatically install
if the application is launched via run.sh.

Once the application and Pytest are installed, in the terminal navigate
to the src folder of the application and in the command line, enter 'pytest'.

7 tests should show as passing - if any errors occur, please contact the app creator.
"""

import builtins
import os
import csv
import random
import io
import unittest.mock

import pytest

import functions


class MockUser:
    """Mock of the User class for testing purposes. Defines the unique variables for each user."""

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


class MockFiles:
    def __init__(self, registered_users, certified_players, previous_results):
        self.registered_users = registered_users
        self.certified_players = certified_players
        self.previous_results = previous_results


"""Test 1: Previous Results"""


@pytest.fixture
def mock_csv_file():
    # Arrange:
    return "User ID,Date,Score,Outcome\n1,2022-01-01,17,Pass\n2,2022-01-02,7,Fail\n"


def test_previous_results(capfd, mock_csv_file):
    """Test Case 1: checking expected results when a previous results file exists with no matches"""
    # Arrange:
    user = MockUser("", "", "3", "", "", "", "")
    # Act
    with unittest.mock.patch(
        "builtins.open", unittest.mock.mock_open(read_data=mock_csv_file)
    ):
        functions.previous_results(user)
    out, err = capfd.readouterr()
    # Assert:
    assert "No previous results available." in out

    """Test Case 2: checking expected results when a previous results file exists with a match"""
    # Arrange:
    user = MockUser("", "", "1", "", "", "", "")
    # Act:
    with unittest.mock.patch(
        "builtins.open", unittest.mock.mock_open(read_data=mock_csv_file)
    ):
        functions.previous_results(user)
    out, err = capfd.readouterr()
    expected_output = (
        "{'User ID': '1', 'Date': '2022-01-01', 'Score': '17', 'Outcome': 'Pass'}"
    )
    # Assert:
    assert any(expected_output in row for row in out.split("\n"))

    """Test Case 3: checking expected results when a previous results file doesn't exist"""
    # Act and assert:
    with unittest.mock.patch("builtins.open", side_effect=FileNotFoundError()):
        with pytest.raises(FileNotFoundError):
            functions.previous_results("test_user")


"""Test 2: Certified Players"""


def test_certified_players():
    """Test Case 1: checking expected results when there is a certified players file"""
    # Arrange:
    players_csv = "tests/test_certified_players.csv"
    with open(players_csv, "w") as f:
        f.write("12345,2023-04-30,2024-10-31")

    # Act and assert:
    with unittest.mock.patch.object(
        builtins, "open", unittest.mock.MagicMock(return_value=open(players_csv, "r"))
    ):
        with unittest.mock.patch("builtins.print") as mock_print:
            functions.certified_players()
            mock_print.assert_called_with("\n12345,2023-04-30,2024-10-31\n")

    # Cleanup:
    os.remove(players_csv)

    """Test Case 2: checking expected results when there is no certified players file"""
    # Act and assert:
    with unittest.mock.patch.object(builtins, "open", side_effect=FileNotFoundError):
        with unittest.mock.patch("builtins.print") as mock_print:
            functions.certified_players()

            expected_output = "\n❗ No certified players on file - please contact WFDF\n"
            mock_print.assert_called_with(expected_output)


"""Test 3: Check Email"""


def test_check_email():
    """Test Case 1: checking expected results with a valid email format"""
    # Arrange:
    user = type("obj", (object,), {"email": "jane.doe@example.com"})
    # Act and assert:
    with unittest.mock.patch("sys.stdout", new=io.StringIO()) as fake_out:
        functions.check_email(user)
        assert fake_out.getvalue() == ""

    """Test Case 2: checking expected results with an invalid email format"""
    # Arrange:
    user = type("obj", (object,), {"email": "janedoe@example"})
    # Act and assert:
    with unittest.mock.patch("builtins.input", return_value="janedoe@example.com"):
        functions.check_email(user)
        assert user.email == "janedoe@example.com"


"""Test 4: Menu Decision"""


def test_menu_selection(monkeypatch, capfd):
    """Test Case 1: checking that an error is caught when str input received"""
    # Arrange:
    monkeypatch.setattr("builtins.input", lambda prompt: next("a"))
    # Act and assert:
    with pytest.raises(TypeError) or pytest.raises(ValueError):
        functions.menu_decision()


"""Test 5: Fail Quiz"""


def test_fail_quiz():
    # Arrange class:
    user = MockUser("", "", "11111", "10", "2023-05-05", "", "")
    files = MockFiles("", "", "")

    """Test Case 1: checking that correct output text is displayed based on user quiz"""
    # Act and assert:
    with unittest.mock.patch("builtins.print") as mock_print:
        functions.fail_quiz_text(user)

        expected_output = (
            "\nYour score was 10/20 and a score of at least 85% is required to pass.\n"
        )
        mock_print.assert_called_with(expected_output)

    """Test Case 2: checking expected results when a previous results file does exist"""
    # Arrange:
    files.previous_results = "tests/test_previous_results.csv"
    with open(files.previous_results, "w") as f:
        f.write("User ID,Date,Score,Outcome\n")
    original_length = 0
    with open(files.previous_results) as f:
        reader = csv.reader(f)
        original_length = sum(1 for row in reader)
    # Act:
    functions.fail_quiz_results(user, files)
    # Assert:
    with open(files.previous_results) as f:
        reader = csv.reader(f)
        new_length = sum(1 for row in reader)
    print(original_length)
    print(new_length)
    assert new_length == original_length + 1
    # Cleanup:
    os.remove(files.previous_results)

    """Test Case 3: checking expected results when a previous results file doesn't exist"""
    # Act and assert:
    with unittest.mock.patch("builtins.open", side_effect=FileNotFoundError()):
        with pytest.raises(FileNotFoundError):
            functions.fail_quiz_results(user, files)


"""Test 6: Pass Quiz"""


def test_pass_quiz():
    # Arrange class:
    user = MockUser("", "", "11111", "17", "2023-05-05", "2024-11-05", "")
    files = MockFiles("", "", "")

    """Test Case 1: checking that correct output text is displayed based on user quiz"""
    # Act and assert:
    with unittest.mock.patch("builtins.print") as mock_print:
        functions.pass_quiz_text(user)

        expected_output = (
            "Your score was 17/20\nYou are now certified until 2024-11-05\n"
        )
        mock_print.assert_called_with(expected_output)

    """Test Case 2: checking expected results when a previous results file does exist"""
    # Arrange:
    files.previous_results = "tests/test_previous_results.csv"
    with open(files.previous_results, "w") as f:
        f.write("User ID,Date,Score,Outcome\n")
    original_length = 0
    with open(files.previous_results) as f:
        reader = csv.reader(f)
        original_length = sum(1 for row in reader)
    # Act:
    functions.pass_quiz_results(user, files)
    # Assert:
    with open(files.previous_results) as f:
        reader = csv.reader(f)
        new_length = sum(1 for row in reader)
    print(original_length)
    print(new_length)
    assert new_length == original_length + 1
    # Cleanup:
    os.remove(files.previous_results)

    """Test Case 3: checking expected results when a previous results file doesn't exist"""
    # Act and assert:
    with unittest.mock.patch("builtins.open", side_effect=FileNotFoundError()):
        with pytest.raises(FileNotFoundError):
            functions.pass_quiz_results(user, files)

    """Test Case 4: checking expected results when a certified players file does exist"""
    # Arrange:
    files.certified_players = "tests/test_certified_players.csv"
    with open(files.certified_players, "w") as f:
        f.write("User ID,Certification Date,Expiry Date\n")
    original_length = 0
    with open(files.certified_players) as f:
        reader = csv.reader(f)
        original_length = sum(1 for row in reader)
    # Act:
    functions.pass_quiz_certified(user, files)
    # Assert:
    with open(files.certified_players) as f:
        reader = csv.reader(f)
        new_length = sum(1 for row in reader)
    print(original_length)
    print(new_length)
    assert new_length == original_length + 1
    # Cleanup:
    os.remove(files.certified_players)

    """Test Case 5: checking expected results when a certified players file doesn't exist"""
    # Act and assert:
    with unittest.mock.patch("builtins.open", side_effect=FileNotFoundError()):
        with pytest.raises(FileNotFoundError):
            functions.pass_quiz_certified(user, files)


"""Test 7: New Quiz"""


def test_new_quiz(monkeypatch):
    """Test Case 1: checking that user score calculation is operating as expected"""
    # Arrange:
    user = MockUser("", "", "", "", "", "", "")
    questions_csv = csv.reader(open("tests/test_quiz_questions.csv", "r"))
    quiz_dict = {}
    for row in questions_csv:
        quiz_dict[row[0]] = row[1:]
    user.questions = random.sample(list(quiz_dict.items()), k=20)
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

    # Act:
    functions.run_quiz(user)
    # Assert:
    assert user.user_score == 13
