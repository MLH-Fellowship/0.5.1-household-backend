from app.models import User


def test_user_passwords():
    user = User()
    user.set_password("password")
    assert user.check_password("password") == True
