from controllers.models import Department, EpicUser
from controllers.mysql import Mysql


class TestMysql:
    def test_init_mysql(self):
        db = Mysql()
        assert db.engine is not None

    def test_has_no_epic_users(self, mysql_instance):
        assert mysql_instance.has_epic_users() == 0

    def test_has_epic_users(self, mysql_instance):
        dept = Department(name="Commercial")
        mysql_instance.session.add(dept)
        user = EpicUser(
            name="Test",
            email="test@example.com",
            password="secret",
            employee_number=1,
            department_id=dept.id
        )
        mysql_instance.session.add(user)
        mysql_instance.session.commit()
        assert mysql_instance.has_epic_users() == 1

    def test_add_user_success(self, mysql_instance):
        dept = Department(name="Management")
        mysql_instance.session.add(dept)
        mysql_instance.session.commit()
        result = mysql_instance.add_user(
            name="Alice",
            email="alice@example.com",
            password="secret",
            employee_number=1,
            department_id=dept.id
        )
        assert result is True
        assert mysql_instance.has_epic_users() == 1

    def test_add_user_duplicate_email(self, mysql_instance):
        dept = Department(name="Marketing")
        mysql_instance.session.add(dept)
        mysql_instance.session.commit()
        mysql_instance.add_user(
            name="Bob",
            email="bob@example.com",
            password="hash1",
            employee_number=2,
            department_id=dept.id
        )
        result = mysql_instance.add_user(
            name="Charlie",
            email="bob@example.com",
            password="hash2",
            employee_number=3,
            department_id=dept.id
        )
        assert result is False
        assert mysql_instance.has_epic_users() == 1

    def test_get_department_list(self, mysql_instance):
        departments = ["RH", "Informatique", "Marketing"]
        for name in departments:
            mysql_instance.session.add(Department(name=name))
        mysql_instance.session.commit()
        assert mysql_instance.get_department_list() == departments

    def test_user_exists(self, mysql_instance):
        # to-do
        assert mysql_instance.user_exists("test", "test") is True
