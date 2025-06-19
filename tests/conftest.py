import locale
import pytest
import jwt
import re
from datetime import datetime, timedelta, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from controllers.models import Base, EpicUser, Client, Contract, Event
from controllers.db import Mysql
from controllers.authentication import Authentication
from controllers.session import Session
from controllers.base import Controller
from views.show import Show
from views.prompt import Ask

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


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
def mysql(db_session, session, authentication):
    mysql = Mysql(session=session, authentication=authentication)
    mysql.db_session = db_session
    return mysql


@pytest.fixture
def session():
    return Session()


@pytest.fixture
def commercial_user():
    return EpicUser(
        name="Commercial",
        email="commercial@example.com",
        employee_number='1',
        department_id=1
    )


@pytest.fixture
def support_user():
    return EpicUser(
        name="Support",
        email="support@example.com",
        employee_number='2',
        department_id=2
    )


@pytest.fixture
def management_user():
    return EpicUser(
        name="Management",
        email="management@example.com",
        employee_number='3',
        department_id=3
    )


@pytest.fixture
def password():
    return 'password'


@pytest.fixture
def client_information():
    return Client(
        name='Nom du contact client',
        email='client@example.fr',
        phone='0202020202',
        company_name='Nom de l\'entreprise'
    )


@pytest.fixture
def contract_information():
    return Contract(
        total_amount=1000,
        rest_amount=1000
    )


@pytest.fixture
def event_information(date_now):
    return Event(
        location='Lieu de l\'évènement',
        attendees='100',
        notes='Note de l\'évènement',
        date_start=date_now,
        date_stop=date_now + timedelta(days=2)
    )


@pytest.fixture
def controller(session, db_session):
    class MyController(Controller):
        def __init__(self, prompt, show, db, auth, session):
            self.session = session
            self.auth = auth(session)
            mysql = Mysql(session=session, authentication=self.auth)
            mysql.db_session = db_session
            self.db = mysql
            self.show = show(self.db, session)
            self.prompt = prompt(self.show, self.db, session)
            self.email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            self.phone_regex = re.compile(r'^\+?[0-9](?:\d{1,3} ?){1,5}\d{1,4}$')
            self.permissions = None

    return MyController(Ask, Show, Mysql, Authentication, session)


@pytest.fixture
def date_now():
    return date.today()


@pytest.fixture
def authentication(monkeypatch, tmp_path, session):
    dovenv_path = tmp_path / '.env'
    dovenv_path.write_text("")
    a = Authentication(session)
    a.dotenv_path = str(dovenv_path)
    return a


def make_token(secret, exp):
    payload = {
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
