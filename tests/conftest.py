import pytest
from sqlalchemy import create_engine
from controllers.models import Base
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
