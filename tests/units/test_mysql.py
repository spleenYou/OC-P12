from controllers.mysql import Mysql
import re


class TestMysql:
    def test_init_mysql(self):
        db = Mysql()
        assert db.engine is not None

    def test_has_no_epic_users(self, mysql_instance):
        assert mysql_instance.has_epic_users() == 0

    def test_has_epic_users(self, mysql_instance, department, epic_user):
        mysql_instance.session.add(epic_user)
        mysql_instance.session.commit()
        assert mysql_instance.has_epic_users() == 1

    def test_add_user_success(self, mysql_instance, department, epic_user):
        mysql_instance.session.commit()
        result = mysql_instance.add_user(
            name="Alice",
            email="alice@example.com",
            password="secret",
            employee_number=1,
            department_id=3
        )
        assert result is True
        assert mysql_instance.has_epic_users() == 1

    def test_add_user_duplicate_email(self, mysql_instance, department):
        mysql_instance.session.commit()
        mysql_instance.add_user(
            name="Bob",
            email="bob@example.com",
            password="hash1",
            employee_number=2,
            department_id=3
        )
        result = mysql_instance.add_user(
            name="Charlie",
            email="bob@example.com",
            password="hash2",
            employee_number=3,
            department_id=3
        )
        assert result is False
        assert mysql_instance.has_epic_users() == 1

    def test_get_department_list(self, mysql_instance):
        departments = ["Commercial", "Support", "Management"]
        assert mysql_instance.get_department_list() == departments

    def test_user_exists(self, mysql_instance, department, epic_user_information):
        mysql_instance.add_user(
            name=epic_user_information['name'],
            email=epic_user_information['email'],
            password=epic_user_information['password'],
            employee_number=epic_user_information['employee_number'],
            department_id=epic_user_information['department_id']
        )
        result = mysql_instance.check_user_login(
            email=epic_user_information['email'],
            password=epic_user_information['password']
        )
        assert result == 1

    def test_user_non_exists(self, mysql_instance, department, epic_user, epic_user_information):
        mysql_instance.session.add(epic_user)
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
