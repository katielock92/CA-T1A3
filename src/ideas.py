#Except error if file goes missing
# confirming that registered users file exists before trying to run login function:
users_file = "./src/registered_users.csv"
try:
    users_file_exists = open(users_file, "r")
    users_file_exists.close()
except FileNotFoundError as e:
    users_file_exists = open(users_file, "w")
    users_file_exists.write("user_email", "user_password", "user_id\n")
    users_file_exists.close()


# test idea
def test_menu_selection(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: next("option"))
    with pytest.raises(ValueError):
        main.menu_decision()