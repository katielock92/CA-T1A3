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




i

def test_new_quiz():
    user = MockUser("", "", "", "", "", "")
    """Test Case 1: checking expected results when the quiz questions file doesn't exist"""
    with patch("builtins.open", side_effect=FileNotFoundError()):
        with pytest.raises(FileNotFoundError):
            functions.check_quiz()