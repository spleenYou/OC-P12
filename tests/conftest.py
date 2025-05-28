import pytest
from sqlalchemy import create_engine
from controllers.models import Base, EpicUser, Department
from controllers.mysql import Mysql
from controllers.base import Controller
from views import show, prompt


class DummyDB:
    def __init__(self, has_users=False):
        self._has_users = has_users
        self.user_created = False

    def has_epic_users(self):
        return self._has_users

    def add_user(self, *args, **kwagrs):
        self.user_created = True
        return True

    def get_department_list(self):
        return ["Commercial", "Support", "Management"]


@pytest.fixture
def controller_no_user():
    db = DummyDB()
    ctrl = Controller(prompt.Prompt, show.Show, lambda: db)
    return ctrl, db


@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    return Base


@pytest.fixture
def mysql_instance(monkeypatch):
    monkeypatch.setenv('DB_USER', 'test')
    monkeypatch.setenv('DB_PASSWORD', 'test')
    monkeypatch.setenv('DB_HOST', 'localhost')
    monkeypatch.setenv('DB_PORT', '3306')
    monkeypatch.setenv('DB_NAME', 'testdb')

    class TestMysql(Mysql):
        def create_engine(self):
            return create_engine('sqlite:///:memory:')

    return TestMysql()


@pytest.fixture
def department():
    return Department(name="Commercial")


@pytest.fixture
def epic_user():
    return EpicUser(
        name="Test",
        email="test@example.com",
        password="secret",
        employee_number=1,
        department_id=1
    )


@pytest.fixture
def epic_user_information():
    return {
        'name': "Test",
        'email': "test@example.com",
        'password': "secret",
        'employee_number': 1,
        'department_id': 1
    }
