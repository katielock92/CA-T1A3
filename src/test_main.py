import functions
import main
import csv

import pytest


test_file_name = "tests/test_users.csv"


#TODO create class and fixture for tests

def test_new_user():
    original_length = 0
    with open(test_file_name) as f:
        reader = csv.reader(f)
        original_length = sum(1 for row in reader)
    functions.user.email = "test@katieelsomlock.com"
    functions.user._password = "Password1234"
    functions.new_user(test_file_name)
    with open(test_file_name) as f:
        reader = csv.reader(f)
        new_length = sum(1 for row in reader)
    print(original_length)
    print(new_length)
    assert new_length == original_length + 1