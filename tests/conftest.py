import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from controllers.models import EpicUser, Client, Contract, Event
from controllers.models import Base
from controllers.db import Mysql
from controllers.authentication import Authentication
from controllers.permissions import Permission
from controllers.session import Session
import jwt
from datetime import datetime, timedelta


@pytest.fixture
def engine():
    return create_engine('sqlite:///:memory:')


@pytest.fixture
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def mysql(db_session, empty_session, authentication):
    mysql = Mysql(session=empty_session, authentication=authentication)
    mysql.db_session = db_session
    return mysql


@pytest.fixture
def commercial_user():
    return {
        'name': "Commercial",
        'email': "commercial@example.com",
        'password': "commercial",
        'employee_number': 1,
        'department_id': 1
    }


@pytest.fixture
def support_user():
    return {
        'name': "Support",
        'email': "support@example.com",
        'password': "support",
        'employee_number': 2,
        'department_id': 2
    }


@pytest.fixture
def management_user():
    return {
        'name': "Management",
        'email': "management@example.com",
        'password': "management",
        'employee_number': 3,
        'department_id': 3
    }


@pytest.fixture
def client_information():
    return {
        'name': 'Nom du client',
        'email': 'client@example.fr',
        'phone': '0202020202',
        'company_name': 'Nom de l\'entreprise'
    }


@pytest.fixture
def contract_information():
    return {
        'total_amount': 1000
    }


@pytest.fixture
def event_information(date_now):
    return {
        'support_contact_id': 2,
        'location': 'Lieu de l\'evènement',
        'attendees': 100,
        'notes': 'Note de l\'evènement',
        'date_start': date_now
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
def authentication(monkeypatch, tmp_path, empty_session):
    dovenv_path = tmp_path / '.env'
    dovenv_path.write_text("")
    a = Authentication(empty_session)
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
