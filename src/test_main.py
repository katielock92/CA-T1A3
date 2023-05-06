import functions

# tidy this up:
import pytest
import builtins
import os
import csv
import random
import tempfile
from unittest import mock
from unittest.mock import Mock, create_autospec
from unittest.mock import MagicMock, patch, mock_open
import io
from io import StringIO


class MockUser:
    """Defines what features each unique user needs.

    Attributes:
        user_id: the unique integer User ID for this user
    """

    def __init__(self, email, password, user_id, user_score, attempt_date, expiry_date):
        """Initialises the instance for each user."""
        self.email = email
        self._password = password
        self.user_id = user_id
        self.user_score = user_score
        self.attempt_date = attempt_date
        self.expiry_date = expiry_date


"""Test 1: Previous Results"""


@pytest.fixture
def mock_csv_file():
    return "User ID,Date,Score,Outcome\n1,2022-01-01,17,Pass\n2,2022-01-02,7,Fail\n"


def test_previous_results(capfd, mock_csv_file):
    """Test Case 1: checking expected results when a previous results file exists with no matches"""
    user = MockUser("", "", "3", "", "", "")
    with patch("builtins.open", mock_open(read_data=mock_csv_file)):
        functions.previous_results(user)
    out, err = capfd.readouterr()
    assert "No previous results available." in out

    """Test Case 2: checking expected results when a previous results file exists with a match"""
    user = MockUser("", "", "1", "", "", "")
    with patch("builtins.open", mock_open(read_data=mock_csv_file)):
        functions.previous_results(user)
    out, err = capfd.readouterr()
    expected_output = (
        "{'User ID': '1', 'Date': '2022-01-01', 'Score': '17', 'Outcome': 'Pass'}"
    )
    assert any(expected_output in row for row in out.split("\n"))

    """Test Case 3: checking expected results when a previous results file doesn't exist"""
    with patch("builtins.open", side_effect=FileNotFoundError()):
        with pytest.raises(FileNotFoundError):
            functions.previous_results("test_user")


"""Test 2: Certified Players"""


def test_certified_players():
    """Test Case 1: checking expected results when there is a certified players file"""
    players_csv = "tests/test_certified_players.csv"
    with open(players_csv, "w") as f:
        f.write("12345,2023-04-30,2024-10-31")

    with patch.object(builtins, "open", MagicMock(return_value=open(players_csv, "r"))):
        with patch("builtins.print") as mock_print:
            functions.certified_players()
            mock_print.assert_called_with("\n12345,2023-04-30,2024-10-31\n")

    os.remove(players_csv)

    """Test Case 2: checking expected results when there is no certified players file"""
    with patch.object(builtins, "open", side_effect=FileNotFoundError):
        with patch("builtins.print") as mock_print:
            functions.certified_players()

            expected_output = "\n❗ No certified players on file - please contact WFDF\n"
            mock_print.assert_called_with(expected_output)


"""Test 3: Check Email"""


def test_check_email():
    """Test Case 1: checking expected results with a valid email format"""
    user = type("obj", (object,), {"email": "jane.doe@example.com"})
    with patch("sys.stdout", new=StringIO()) as fake_out:
        functions.check_email(user)
        assert fake_out.getvalue() == ""

    """Test Case 2: checking expected results with an invalid email format"""
    user = type("obj", (object,), {"email": "janedoe@example"})
    with patch("builtins.input", return_value="janedoe@example.com"):
        functions.check_email(user)
        assert user.email == "janedoe@example.com"


"""Test 4: Menu Decision"""


def test_menu_selection(monkeypatch):
    """Test Case 1: checking that an error is caught when str input received"""
    monkeypatch.setattr("builtins.input", lambda _: next("a"))
    with pytest.raises(TypeError) or pytest.raises(ValueError):
        functions.menu_decision()

    # TODO add test case for invalid number - currently getting a type error


"""Test 5: Fail Quiz"""


def test_fail_quiz():
    user = MockUser("", "", "11111", "10", "2023-05-05", "")

    """Test Case 1: checking that correct output text is displayed based on user quiz"""
    with patch("builtins.print") as mock_print:
        functions.fail_quiz_text(user)

        expected_output = (
            "\nYour score was 10/20 and a score of at least 85% is required to pass.\n"
        )
        mock_print.assert_called_with(expected_output)

    """Test Case 2: checking expected results when a previous results file does exist"""
    # TODO mock write to file and check it has the expected output

    """Test Case 3: checking expected results when a previous results file doesn't exist"""
    with patch("builtins.open", side_effect=FileNotFoundError()):
        with pytest.raises(FileNotFoundError):
            functions.fail_quiz_results(user)


"""Test 6: Pass Quiz"""


def test_pass_quiz():
    user = MockUser("", "", "11111", "17", "2023-05-05", "2024-11-05")

    """Test Case 1: checking that correct output text is displayed based on user quiz"""
    with patch("builtins.print") as mock_print:
        functions.pass_quiz_text(user)

        expected_output = "You are now certified until 2024-11-05"
        mock_print.assert_called_with(expected_output)

    """Test Case 2: checking expected results when a previous results file does exist"""
    # TODO mock write to file and check it has the expected output

    """Test Case 3: checking expected results when a previous results file doesn't exist"""
    with patch("builtins.open", side_effect=FileNotFoundError()):
        with pytest.raises(FileNotFoundError):
            functions.pass_quiz_results(user)

    """Test Case 4: checking expected results when a certified players file does exist"""
    # TODO mock write to file and check it has the expected output

    """Test Case 5: checking expected results when a certified players file doesn't exist"""
    with patch("builtins.open", side_effect=FileNotFoundError()):
        with pytest.raises(FileNotFoundError):
            functions.pass_quiz_certified(user)


"""Test 7: New Quiz"""
