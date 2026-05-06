from unittest.mock import MagicMock
from auth import get_current_user


def test_get_current_user_mock():
    fake_db = MagicMock()

    fake_user = MagicMock()
    fake_user.id = 1
    fake_user.name = "test"

    fake_db.query().filter().first.return_value = fake_user

    user = fake_db.query().filter().first()

    assert user.id == 1
    assert user.name == "test"
