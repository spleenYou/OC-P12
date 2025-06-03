import pytest
from sqlalchemy import create_engine
from controllers.models import Base, EpicUser
from controllers.mysql import Mysql
from controllers.base import Controller
from views import show, prompt
from controllers.authentication import Authentication
from controllers.permissions import Check_Permission
import jwt
from datetime import datetime, timedelta


@pytest.fixture
def controller(mysql_instance, epic_user_information):
    return Controller(
        prompt.Prompt,
        show.Show,
        lambda: mysql_instance,
        Authentication
    )


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
def epic_user_information():
    return {
        'name': "Test",
        'email': "test@example.com",
        'password': "secret",
        'employee_number': 1,
        'department_id': 1
    }


@pytest.fixture
def empty_user():
    return EpicUser()


@pytest.fixture
def authentication(monkeypatch, tmp_path):
    dovenv_path = tmp_path / '.env'
    dovenv_path.write_text("")
    a = Authentication()
    a.dotenv_path = str(dovenv_path)
    return a


@pytest.fixture
def permissions():
    db = Mysql()
    return Check_Permission(db.get_permissions())


def make_token(secret, exp):
    payload = {
        'department_id': 1,
        'exp': exp
    }
    return jwt.encode(payload=payload, key=secret, algorithm='HS256')


@pytest.fixture
def secret():
    return 'my_secret_key'


@pytest.fixture
def token(secret):
    return make_token(secret=secret, exp=datetime.utcnow() + timedelta(hours=1))


@pytest.fixture
def invalid_token(secret):
    return make_token(secret=secret, exp=datetime.utcnow() - timedelta(hours=1))
