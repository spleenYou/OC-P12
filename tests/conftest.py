import pytest
from sqlalchemy import create_engine
from controllers.models import Base, EpicUser, Department
from controllers.mysql import Mysql
from controllers.base import Controller
from views import show, prompt
from controllers.authentication import Authentication
from controllers.permission import Permission


@pytest.fixture
def controller(mysql_instance):
    return Controller(prompt.Prompt, show.Show, lambda: mysql_instance, Authentication, Permission)


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
    return Permission(db)
