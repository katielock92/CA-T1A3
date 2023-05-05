import functions

import pytest
import builtins
import os
from unittest.mock import MagicMock, patch

"""Test 1: Previous Results"""
def test_previous_results():
    """Test Case 1: checking expected results when there is a previous results file"""
    results_csv = "tests/test_previous_results.csv"
    with open(results_csv, "w") as f:
        f.write("2023-04-30,17,Pass")

    with patch.object(
        builtins, "open", MagicMock(return_value=open(results_csv, "r"))
    ):
        with patch("builtins.print") as mock_print:
            functions.previous_results()

            mock_print.assert_called_with("2023-04-30,17,Pass")

    
    os.remove(results_csv)

    """Test Case 2: checking expected results when there is no previous results file"""
    with patch.object(builtins, "open", side_effect=FileNotFoundError):
        with patch("builtins.print") as mock_print:
            functions.previous_results()

            expected_output = "\nNo previous results available.\n"
            mock_print.assert_called_with(expected_output)

"""Test 2: Certified Players"""
def test_certified_players():
    """Test Case 1: checking expected results when there is a certified players file"""
    players_csv = "tests/test_certified_players.csv"
    with open(players_csv, "w") as f:
        f.write("12345, 2023-04-30, 2024-10-31")

    with patch.object(
        builtins, "open", MagicMock(return_value=open(players_csv, "r"))
    ):
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
