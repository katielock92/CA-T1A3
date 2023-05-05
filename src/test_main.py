import functions

import pytest
import builtins
import os
from unittest.mock import MagicMock, patch, mock_open


class MockUser:
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


"""Test 1: Previous Results"""

@pytest.fixture
def mock_csv_file():
    return "User ID,Date,Score,Outcome\n1,2022-01-01,17,Pass\n2,2022-01-02,7,Fail\n"

def test_previous_results(capfd, mock_csv_file):
    """Test Case 1: checking expected results when a previous results file exists with no matches"""
    user = MockUser("", "", "3", "")
    with patch("builtins.open", mock_open(read_data=mock_csv_file)):
        functions.previous_results(user)
    out, err = capfd.readouterr()
    assert "No previous results available." in out


    """Test Case 2: checking expected results when a previous results file exists with a match"""
    user = MockUser("", "", "1", "")
    with patch("builtins.open", mock_open(read_data=mock_csv_file)):
        functions.previous_results(user)
    out, err = capfd.readouterr()
    expected_output = "{'User ID': '1', 'Date': '2022-01-01', 'Score': '17', 'Outcome': 'Pass'}"
    assert any(expected_output in row for row in out.split("\n"))

    """Test Case 3: checking expected results when a previous results file doesn't exist"""
    with patch('builtins.open', side_effect=FileNotFoundError()):
        with pytest.raises(FileNotFoundError):
            functions.previous_results("test_user")


"""Test 2: Certified Players"""


def test_certified_players():
    """Test Case 1: checking expected results when there is a certified players file"""
    players_csv = "tests/test_certified_players.csv"
    with open(players_csv, "w") as f:
        f.write("12345, 2023-04-30, 2024-10-31")

    with patch.object(builtins, "open", MagicMock(return_value=open(players_csv, "r"))):
        with patch("builtins.print") as mock_print:
            functions.certified_players()

            mock_print.assert_called_with("12345, 2023-04-30, 2024-10-31")

    os.remove(players_csv)

    """Test Case 2: checking expected results when there is no certified players file"""
    with patch.object(builtins, "open", side_effect=FileNotFoundError):
        with patch("builtins.print") as mock_print:
            functions.certified_players()

            expected_output = "\nNo certified players on file - please contact WFDF\n"
            mock_print.assert_called_with(expected_output)

