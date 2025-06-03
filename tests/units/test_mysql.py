import re
from datetime import datetime, timedelta
import jwt
from controllers.mysql import Mysql
from controllers.models import EpicUser


class TestMysql:
    def add_users(self, db):
        db.add_user(
            name="Alice",
            email="alice@example.com",
            password="hash1",
            employee_number=1,
            department_id=3
        )
        db.add_user(
            name="Bob",
            email="bob@example.com",
            password="hash1",
            employee_number=2,
            department_id=2
        )
        db.add_user(
            name="Conrad",
            email="conrad@example.com",
            password="hash1",
            employee_number=3,
            department_id=1
        )

    def test_init_mysql(self):
        db = Mysql()
        assert db.engine is not None

    def test_has_no_epic_users(self, mysql_instance):
        assert mysql_instance.has_epic_users() == 0

    def test_has_epic_users(self, mysql_instance, epic_user_information):
        mysql_instance.session.add(EpicUser(**epic_user_information))
        mysql_instance.session.commit()
        assert mysql_instance.has_epic_users() == 1

    def make_token(self, secret, exp):
        payload = {
            'department_id': 1,
            'exp': exp
        }
        return jwt.encode(payload=payload, key=secret, algorithm='HS256')

    def test_add_in_db_ok(self, mysql_instance, epic_user_information, monkeypatch):
        new_user = EpicUser(**epic_user_information)
        secret = 'my_secret_key'
        token = self.make_token(secret=secret, exp=datetime.utcnow() + timedelta(hours=1))
        monkeypatch.setattr(
            target='controllers.authentication.get_key',
            name=lambda path, key: secret if key == 'SECRET_KEY' else token
        )
        result = mysql_instance.add_in_db(new_user)
        assert result == 1

    def test_add_in_db_failed(self, mysql_instance, epic_user_information, monkeypatch):
        secret = 'my_secret_key'
        token = self.make_token(secret=secret, exp=datetime.utcnow() + timedelta(hours=1))
        monkeypatch.setattr(
            target='controllers.authentication.get_key',
            name=lambda path, key: secret if key == 'SECRET_KEY' else token
        )
        mysql_instance.add_in_db(EpicUser(**epic_user_information))
        result = mysql_instance.add_in_db(EpicUser(**epic_user_information))
        assert result is False

    def test_get_department_list(self, mysql_instance):
        departments = ["Commercial", "Support", "Management"]
        assert mysql_instance.get_department_list() == departments

    def test_user_login_ok(self, mysql_instance, epic_user_information):
        user = EpicUser(
            name=epic_user_information['name'],
            email=epic_user_information['email'],
            employee_number=epic_user_information['employee_number'],
            department_id=epic_user_information['department_id'],
            password=mysql_instance.hash_password(epic_user_information['password'])
        )
        mysql_instance.add_in_db(user)
        result = mysql_instance.check_user_login(
            email=epic_user_information['email'],
            password=epic_user_information['password']
        )
        assert result == user

    def test_user_login_with_wrong_email(self, mysql_instance, epic_user_information):
        mysql_instance.session.add(EpicUser(**epic_user_information))
        result = mysql_instance.check_user_login(
            email=epic_user_information['email'] + "e",
            password=epic_user_information['password']
        )
        assert result is None

    def test_user_login_with_wrong_password(self, mysql_instance, epic_user_information):
        mysql_instance.session.add(EpicUser(**epic_user_information))
        result = mysql_instance.check_user_login(
            email=epic_user_information['email'],
            password=epic_user_information['password'] + "e"
        )
        assert result is None

    def test_hash_password(self, mysql_instance, epic_user_information):
        hash_password = mysql_instance.hash_password(epic_user_information['password'])
        assert re.search(
            "[$]{1}argon2id[$]{1}v=19[$]{1}m=65536,t=4,p=1[$]{1}[+.\x00-9a-zA-Z]{22}[$]{1}[+.\x00-9a-zA-Z]{43}",
            hash_password
        ) is not None

    def test_password_verification(self, mysql_instance, epic_user_information):
        hash_password = mysql_instance.hash_password(epic_user_information['password'])
        assert mysql_instance.password_verification(epic_user_information['password'], hash_password) is True

    def test_password_verification_fail(self, mysql_instance, epic_user_information):
        hash_password = mysql_instance.hash_password(epic_user_information['password'] + "e")
        assert mysql_instance.password_verification(epic_user_information['password'], hash_password) is False
