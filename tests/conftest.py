import pytest
from sqlalchemy import create_engine
from controllers.models import Base, EpicUser, Department
from controllers.mysql import Mysql


@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    return Base


@pytest.fixture
def mysql_instance(monkeypatch):
    """Fixture qui surcharge la connexion MySQL par SQLite en mémoire"""
    # Mock des variables d'environnement
    monkeypatch.setenv('DB_USER', 'test')
    monkeypatch.setenv('DB_PASSWORD', 'test')
    monkeypatch.setenv('DB_HOST', 'localhost')
    monkeypatch.setenv('DB_PORT', '3306')
    monkeypatch.setenv('DB_NAME', 'testdb')

    # Classe enfant qui surcharge create_engine()
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
