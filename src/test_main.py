import functions
import csv

import pytest


test_file_name = "tests/test_users.csv"


def test_new_user(monkeypatch):
    original_length = 0
    with open(test_file_name) as f:
        reader = csv.reader(f)
        original_length = sum(1 for row in reader)
    inputs = iter(["test@katieelsomlock.com", "Password1234", "12345"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    functions.new_user()
    with open(test_file_name) as f:
        reader = csv.reader(f)
        new_length = sum(1 for row in reader)
    print(original_length)
    print(new_length)
    assert new_length == original_length + 1
