import pytest
from sqlalchemy import create_engine
from controllers.models import EpicUser, Client, Contract, Event
from controllers.db import Mysql
from controllers.authentication import Authentication
from controllers.permissions import Permission
from controllers.session import Session
import jwt
from datetime import datetime, timedelta


@pytest.fixture
def mysql_instance(monkeypatch):
    monkeypatch.setenv('DB_USER', 'test')
    monkeypatch.setenv('DB_PASSWORD', 'test')
    monkeypatch.setenv('DB_HOST', 'localhost')
    monkeypatch.setenv('DB_PORT', '3306')
    monkeypatch.setenv('DB_NAME', 'testdb')
    session = Session()
    db = Mysql(session)

    class TestMysql(db):
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
def empty_client():
    return Client()


@pytest.fixture
def empty_contract():
    return Contract()


@pytest.fixture
def empty_event():
    return Event()


@pytest.fixture
def date_now():
    return datetime.now()


@pytest.fixture
def empty_session():
    return Session()


@pytest.fixture
def authentication(monkeypatch, tmp_path, session):
    dovenv_path = tmp_path / '.env'
    dovenv_path.write_text("")
    a = Authentication(session)
    a.dotenv_path = str(dovenv_path)
    return a


@pytest.fixture
def permissions():
    db = Mysql()
    return Permission(db.get_permissions())


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
