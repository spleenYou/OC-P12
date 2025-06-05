import re
from controllers.db import Mysql
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

    def test_get_epic_user_information(self, mysql_instance):
        mysql_instance.add_epic_user(
            name='test',
            email='test@example.com',
            password='password',
            employee_number=1,
            department_id=1
        )
        user_information = mysql_instance.get_epic_user_information('test@example.com',)
        assert re.search(
            "[$]{1}argon2id[$]{1}v=19[$]{1}m=65536,t=4,p=1[$]{1}[+.\x00-9a-zA-Z]{22}[$]{1}[+.\x00-9a-zA-Z]{43}",
            user_information.password
        ) is not None

    def test_add_in_db_ok(self, mysql_instance, epic_user_information, monkeypatch, secret, token):
        new_user = EpicUser(**epic_user_information)
        monkeypatch.setattr(
            target='controllers.authentication.get_key',
            name=lambda path, key: secret if key == 'SECRET_KEY' else token
        )
        result = mysql_instance.add_in_db(new_user)
        assert result == 1

    def test_add_in_db_failed(self, mysql_instance, epic_user_information, monkeypatch, secret, token):
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

    def test_add_user(self, mysql_instance):
        result = mysql_instance.add_epic_user(
            name='test',
            email='test@example.com',
            password='password',
            employee_number=1,
            department_id=1
        )
        assert result is True

    def test_update_user(self, mysql_instance, empty_client):
        result = mysql_instance.update_epic_user(
            epic_user=empty_client,
            name='test',
            email='test@example.com',
            password='password',
            employee_number=1,
            department_id=1
        )
        assert result is True

    def test_update_user_failed(self, mysql_instance):
        result = mysql_instance.update_epic_user(
            epic_user=None
        )
        assert result is False

    def test_get_epic_user_list(self, mysql_instance):
        mysql_instance.add_epic_user(
            name='test',
            email='test@example.com',
            password='password',
            employee_number=1,
            department_id=1
        )
        result = mysql_instance.get_epic_user_list()
        assert len(result) != 0
        assert result[0].name == 'test'
        assert result[0].email == 'test@example.com'
        assert mysql_instance.auth.check_password('password', result[0].password) is True
        assert result[0].employee_number == 1
        assert result[0].department_id == 1

    def test_delete_epic_user(self, mysql_instance):
        mysql_instance.add_epic_user(
            name='test',
            email='test@example.com',
            password='password',
            employee_number=1,
            department_id=1
        )
        users = mysql_instance.get_epic_user_list()
        assert mysql_instance.has_epic_users() == 1
        result = mysql_instance.delete_epic_user(users[0])
        assert result is True
        assert mysql_instance.has_epic_users() == 0

    def test_delete_epic_user_failed(self, mysql_instance):
        mysql_instance.add_epic_user(
            name='test',
            email='test@example.com',
            password='password',
            employee_number=1,
            department_id=1
        )
        assert mysql_instance.delete_epic_user(None) is False

    def test_add_client(self, mysql_instance):
        result = mysql_instance.add_client(
            name='Antoine',
            email='client@example.com',
            phone='0202020202',
            entreprise_name='Entreprise 1',
            commercial_contact_id=1
        )
        assert result is True

    def test_update_client(self, mysql_instance, empty_client):
        result = mysql_instance.update_client(
            empty_client,
            name='test',
            email='test@example.com',
            phone='0202020202',
            entreprise_name='Entreprise A',
            commercial_contact_id=1
        )
        assert result is True

    def test_update_client_failed(self, mysql_instance):
        result = mysql_instance.update_client(
            None
        )
        assert result is False

    def test_delete_client(self, mysql_instance, empty_client):
        empty_client.id = 1
        mysql_instance.add_client(
            name='Antoine',
            email='client@example.com',
            phone='0202020202',
            entreprise_name='Entreprise 1',
            commercial_contact_id=1
        )
        clients = mysql_instance.get_client_list()
        assert len(clients) == 1
        assert mysql_instance.delete_client(clients[0]) is True
        assert len(mysql_instance.get_client_list()) == 0

    def test_delete_client_failed(self, mysql_instance, empty_client):
        mysql_instance.add_client(
            name='Antoine',
            email='client@example.com',
            phone='0202020202',
            entreprise_name='Entreprise 1',
            commercial_contact_id=1
        )
        assert mysql_instance.delete_client(None) is False

    def test_get_client_list(self, mysql_instance):
        mysql_instance.add_client(
            name='test',
            email='test@example.com',
            phone='0202020202',
            entreprise_name='Entreprise A',
            commercial_contact_id=1
        )
        result = mysql_instance.get_client_list()
        assert len(result) != 0
        assert result[0].name == 'test'
        assert result[0].email == 'test@example.com'
        assert result[0].entreprise_name == 'Entreprise A'
        assert result[0].commercial_contact_id == 1

    def test_add_contract(self, mysql_instance):
        result = mysql_instance.add_contract(
            client_id=1,
            total_amount=1000,
            rest_amount=1000
        )
        assert result is True

    def test_update_contract(self, mysql_instance, empty_contract):
        result = mysql_instance.update_contract(
            empty_contract,
            client_id=1,
            total_amount=1000,
            rest_amount=1000,
            status=True
        )
        assert result is True

    def test_update_contract_failed(self, mysql_instance):
        result = mysql_instance.update_contract(
            None
        )
        assert result is False

    def test_delete_contract(self, mysql_instance, empty_contract, empty_client):
        empty_contract.id = 1
        empty_client.id = 1
        mysql_instance.add_contract(
            client_id=1,
            total_amount=1000,
            rest_amount=1000,
        )
        contracts = mysql_instance.get_contract_list(empty_client)
        assert len(contracts) == 1
        assert mysql_instance.delete_contract(contracts[0]) is True
        assert len(mysql_instance.get_contract_list(empty_client)) == 0

    def test_delete_contract_failed(self, mysql_instance):
        assert mysql_instance.delete_contract(None) is False

    def test_get_contract_list(self, mysql_instance, empty_client):
        empty_client.id = 1
        mysql_instance.add_contract(
            client_id=1,
            total_amount=1000,
            rest_amount=1000,
        )
        result = mysql_instance.get_contract_list(empty_client)
        assert len(result) != 0
        assert result[0].client_id == 1
        assert result[0].total_amount == 1000
        assert result[0].rest_amount == 1000

    def test_add_event(self, mysql_instance, date_now):
        result = mysql_instance.add_event(
            contract_id=1,
            support_contact_id=1,
            location='endroit',
            attendees=100,
            notes='Ne pas oublier',
            date_start=date_now
        )
        assert result is True

    def test_update_event(self, mysql_instance, empty_event, date_now):
        result = mysql_instance.update_event(
            empty_event,
            contract_id=1,
            support_contact_id=1,
            location='endroit',
            attendees=100,
            notes='Ne pas oublier',
            date_start=date_now,
            date_stop=date_now
        )
        assert result is True

    def test_update_event_failed(self, mysql_instance):
        result = mysql_instance.update_event(
            None
        )
        assert result is False

    def test_delete_event(self, mysql_instance, date_now):
        mysql_instance.add_epic_user(
            name='test',
            email='test@example.com',
            password='password',
            employee_number=1,
            department_id=1
        )
        mysql_instance.add_client(
            name='Antoine',
            email='client@example.com',
            phone='0202020202',
            entreprise_name='Entreprise 1',
            commercial_contact_id=1
        )
        mysql_instance.add_contract(
            client_id=1,
            total_amount=1000,
            rest_amount=1000
        )
        mysql_instance.add_event(
            contract_id=1,
            support_contact_id=1,
            location='endroit',
            attendees=100,
            notes='Ne pas oublier',
            date_start=date_now
        )
        events = mysql_instance.get_event_list_by_client(1)
        print(events)
        assert len(events) == 1
        assert mysql_instance.delete_event(events[0]) is True
        assert len(mysql_instance.get_event_list_by_client(1)) == 0

    def test_delete_event_failed(self, mysql_instance):
        assert mysql_instance.delete_event(None) is False

    def test_get_event_list_by_client(self, mysql_instance, empty_contract, date_now):
        mysql_instance.add_epic_user(
            name='test',
            email='test@example.com',
            password='password',
            employee_number=1,
            department_id=1
        )
        mysql_instance.add_client(
            name='Antoine',
            email='client@example.com',
            phone='0202020202',
            entreprise_name='Entreprise 1',
            commercial_contact_id=1
        )
        mysql_instance.add_contract(
            client_id=1,
            total_amount=1000,
            rest_amount=1000
        )
        mysql_instance.add_event(
            contract_id=1,
            support_contact_id=1,
            location='endroit',
            attendees=100,
            notes='Ne pas oublier',
            date_start=date_now
        )
        result = mysql_instance.get_event_list_by_client(1)
        assert len(result) != 0

    def test_get_event_list_by_epic_user(self, mysql_instance, empty_contract, date_now):
        mysql_instance.add_epic_user(
            name='test',
            email='test@example.com',
            password='password',
            employee_number=1,
            department_id=1
        )
        mysql_instance.add_client(
            name='Antoine',
            email='client@example.com',
            phone='0202020202',
            entreprise_name='Entreprise 1',
            commercial_contact_id=1
        )
        mysql_instance.add_contract(
            client_id=1,
            total_amount=1000,
            rest_amount=1000
        )
        mysql_instance.add_event(
            contract_id=1,
            support_contact_id=1,
            location='endroit',
            attendees=100,
            notes='Ne pas oublier',
            date_start=date_now
        )
        result = mysql_instance.get_event_list_by_epic_user(1)
        assert len(result) != 0
