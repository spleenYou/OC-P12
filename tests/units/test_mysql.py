import re
from controllers.db import Mysql
from controllers.models import EpicUser


class TestMysql:
    def add_user(self, db, user):
        db.session.new_user['name'] = user['name']
        db.session.new_user['email'] = user['email']
        db.session.new_user['password'] = user['password']
        db.session.new_user['employee_number'] = user['employee_number']
        db.session.new_user['department_id'] = user['department_id']
        db.add_user()

    def add_client(self, db, client):
        db.session.client['name'] = client['name']
        db.session.client['email'] = client['email']
        db.session.client['phone'] = client['phone']
        db.session.client['company_name'] = client['company_name']
        db.add_client()

    def add_contract(self, db, contract):
        db.session.contract['total_amount'] = contract['total_amount']
        db.add_contract()

    def test_init_mysql(self, empty_session, authentication):
        db = Mysql(empty_session, authentication)
        assert db.engine is not None

    def test_has_users_empty(self, mysql):
        assert mysql.has_users() == 0

    def test_has_users(self, mysql, management_user):
        mysql.db_session.add(EpicUser(**management_user))
        mysql.db_session.commit()
        assert mysql.has_users() == 1

    def test_get_user_information(self, mysql, management_user):
        self.add_user(mysql, management_user)
        mysql.session.user = mysql.session.new_user
        password = mysql.get_user_password()
        assert re.search(
            "[$]{1}argon2id[$]{1}v=19[$]{1}m=65536,t=4,p=1[$]{1}[+.\x00-9a-zA-Z]{22}[$]{1}[+.\x00-9a-zA-Z]{43}",
            password
        ) is not None

    def test_add_in_db_ok(self, mysql, management_user, monkeypatch, secret):
        new_user = EpicUser(**management_user)
        monkeypatch.setattr(
            target='controllers.authentication.get_key',
            name=lambda path, key: secret
        )
        result = mysql.add_in_db(new_user)
        assert result == 1

    def test_add_in_db_failed(self, mysql, management_user, monkeypatch, secret):
        monkeypatch.setattr(
            target='controllers.authentication.get_key',
            name=lambda path, key: secret
        )
        mysql.add_in_db(EpicUser(**management_user))
        result = mysql.add_in_db(EpicUser(**management_user))
        assert result is False

    def test_get_department_list(self, mysql):
        departments = ["Commercial", "Support", "Management"]
        assert mysql.get_department_list() == departments

    def test_update_user(self, mysql, management_user):
        self.add_user(mysql, management_user)
        result = mysql.get_user_information(management_user['email'])
        assert result['name'] == management_user['name']
        mysql.session.new_user = result
        mysql.session.new_user['name'] = 'Nouveau nom'
        result = mysql.update_user()
        assert result is True
        result = mysql.get_user_information(management_user['email'])
        assert result['name'] == 'Nouveau nom'

    def test_update_user_failed(self, mysql, db_session, management_user):
        self.add_user(mysql, management_user)
        mysql.session.new_user['id'] = 2
        result = mysql.update_user()
        assert result is False

    def test_get_user_list(self, mysql, management_user):
        self.add_user(mysql, management_user)
        result = mysql.get_user_list()
        assert len(result) != 0
        assert result[0].name == management_user['name']
        assert result[0].email == management_user['email']
        assert mysql.auth.check_password(management_user['password'], result[0].password) is True
        assert result[0].employee_number == management_user['employee_number']
        assert result[0].department_id == management_user['department_id']

    def test_delete_user(self, mysql, management_user):
        self.add_user(mysql, management_user)
        users = mysql.get_user_list()
        assert mysql.has_users() == 1
        result = mysql.delete_user(users[0].id)
        assert result is True
        assert mysql.has_users() == 0

    def test_delete_user_failed(self, mysql):
        assert mysql.delete_user(1) is False

    def test_add_client(self, mysql, commercial_user):
        self.add_user(mysql, commercial_user)
        mysql.session.user = mysql.get_user_information(commercial_user['email'])
        mysql.session.client['name'] = 'Nom du client'
        mysql.session.client['email'] = 'client@example.com'
        mysql.session.client['phone'] = '0202020202'
        mysql.session.client['company_name'] = 'Nom de l\'entreprise du client'
        result = mysql.add_client()
        assert result is True

    def test_update_client(self, mysql, commercial_user, client_information):
        self.add_user(mysql, commercial_user)
        mysql.session.user = mysql.get_user_information(commercial_user['email'])
        self.add_client(mysql, client_information)
        client = mysql.get_client_information(1)
        mysql.session.client = mysql.get_client_information(client['id'])
        assert client['name'] == client_information['name']
        mysql.session.client['name'] = 'Nouveau nom'
        result = mysql.update_client(client['id'])
        assert result is True
        client = mysql.get_client_information(client['id'])
        assert client['name'] == 'Nouveau nom'

    def test_update_client_failed(self, mysql, commercial_user, client_information):
        self.add_user(mysql, commercial_user)
        mysql.session.user = mysql.get_user_information(commercial_user['email'])
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client_information(1)
        result = mysql.update_client(2)
        assert result is False

    def test_delete_client(self, mysql, commercial_user, client_information):
        self.add_user(mysql, commercial_user)
        mysql.session.user = mysql.get_user_information(commercial_user['email'])
        self.add_client(mysql, client_information)
        clients = mysql.get_client_list()
        assert len(clients) == 1
        assert mysql.delete_client(clients[0].id) is True
        assert len(mysql.get_client_list()) == 0

    def test_delete_client_failed(self, mysql, commercial_user, client_information):
        self.add_user(mysql, commercial_user)
        mysql.session.user = mysql.get_user_information(commercial_user['email'])
        self.add_client(mysql, client_information)
        clients = mysql.get_client_list()
        assert len(clients) == 1
        assert mysql.delete_client(clients[0].id + 1) is False
        assert len(mysql.get_client_list()) == 1

    def test_get_client_list(self, mysql, commercial_user, client_information):
        self.add_user(mysql, commercial_user)
        mysql.session.user = mysql.get_user_information(commercial_user['email'])
        self.add_client(mysql, client_information)
        clients = mysql.get_client_list()
        assert len(clients) != 0
        assert clients[0].name == client_information['name']
        assert clients[0].email == client_information['email']
        assert clients[0].company_name == client_information['company_name']
        assert clients[0].commercial_contact_id == 1

    def test_add_contract(self, mysql, commercial_user, client_information, contract_information):
        self.add_user(mysql, commercial_user)
        mysql.session.user = mysql.get_user_information(commercial_user['email'])
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client_information(1)
        mysql.session.contract['total_amount'] = contract_information['total_amount']
        result = mysql.add_contract()
        assert result is True

    def test_update_contract(self, mysql, commercial_user, client_information, contract_information):
        self.add_user(mysql, commercial_user)
        mysql.session.user = mysql.get_user_information(commercial_user['email'])
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client_information(1)
        self.add_contract(mysql, contract_information)
        mysql.session.contract = mysql.get_contract_information(1)
        assert mysql.session.contract['rest_amount'] == contract_information['total_amount']
        mysql.session.contract['rest_amount'] = 500
        result = mysql.update_contract(1)
        assert result is True
        mysql.session.contract = mysql.get_contract_information(1)
        assert mysql.session.contract['rest_amount'] == 500

    def test_update_contract_failed(self, mysql, commercial_user, client_information, contract_information):
        self.add_user(mysql, commercial_user)
        mysql.session.user = mysql.get_user_information(commercial_user['email'])
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client_information(1)
        self.add_contract(mysql, contract_information)
        mysql.session.contract = mysql.get_contract_information(1)
        assert mysql.session.contract['rest_amount'] == contract_information['total_amount']
        mysql.session.contract['rest_amount'] = 500
        result = mysql.update_contract(2)
        assert result is False

    def test_delete_contract(self, mysql, commercial_user, client_information, contract_information):
        self.add_user(mysql, commercial_user)
        mysql.session.user = mysql.get_user_information(commercial_user['email'])
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client_information(1)
        self.add_contract(mysql, contract_information)
        mysql.session.contract = mysql.get_contract_information(1)
        contracts = mysql.get_contract_list()
        assert len(contracts) == 1
        assert mysql.delete_contract(contracts[0].id) is True
        assert len(mysql.get_contract_list()) == 0

    def test_delete_contract_failed(self, mysql, commercial_user, client_information, contract_information):
        self.add_user(mysql, commercial_user)
        mysql.session.user = mysql.get_user_information(commercial_user['email'])
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client_information(1)
        self.add_contract(mysql, contract_information)
        contracts = mysql.get_contract_list()
        assert len(contracts) == 1
        assert mysql.delete_contract(contracts[0].id + 1) is False
        assert len(mysql.get_contract_list()) == 1

    def test_get_contract_list(self, mysql, commercial_user, client_information, contract_information):
        self.add_user(mysql, commercial_user)
        mysql.session.user = mysql.get_user_information(commercial_user['email'])
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client_information(1)
        self.add_contract(mysql, contract_information)
        result = mysql.get_contract_list()
        assert len(result) != 0
        assert result[0].client_id == mysql.session.client['id']
        assert result[0].total_amount == contract_information['total_amount']
        assert result[0].rest_amount == contract_information['total_amount']

    # def test_add_event(self, mysql, date_now):
    #     result = mysql.add_event(
    #         contract_id=1,
    #         support_contact_id=1,
    #         location='endroit',
    #         attendees=100,
    #         notes='Ne pas oublier',
    #         date_start=date_now
    #     )
    #     assert result is True

    # def test_update_event(self, mysql, empty_event, date_now):
    #     result = mysql.update_event(
    #         empty_event,
    #         contract_id=1,
    #         support_contact_id=1,
    #         location='endroit',
    #         attendees=100,
    #         notes='Ne pas oublier',
    #         date_start=date_now,
    #         date_stop=date_now
    #     )
    #     assert result is True

    # def test_update_event_failed(self, mysql):
    #     result = mysql.update_event(
    #         None
    #     )
    #     assert result is False

    # def test_delete_event(self, mysql, date_now):
    #     mysql.add_user(
    #         name='test',
    #         email='test@example.com',
    #         password='password',
    #         employee_number=1,
    #         department_id=1
    #     )
    #     mysql.add_client(
    #         name='Antoine',
    #         email='client@example.com',
    #         phone='0202020202',
    #         entreprise_name='Entreprise 1',
    #         commercial_contact_id=1
    #     )
    #     mysql.add_contract(
    #         client_id=1,
    #         total_amount=1000,
    #         rest_amount=1000
    #     )
    #     mysql.add_event(
    #         contract_id=1,
    #         support_contact_id=1,
    #         location='endroit',
    #         attendees=100,
    #         notes='Ne pas oublier',
    #         date_start=date_now
    #     )
    #     events = mysql.get_event_list_by_client(1)
    #     print(events)
    #     assert len(events) == 1
    #     assert mysql.delete_event(events[0]) is True
    #     assert len(mysql.get_event_list_by_client(1)) == 0

    # def test_delete_event_failed(self, mysql):
    #     assert mysql.delete_event(None) is False

    # def test_get_event_list_by_client(self, mysql, empty_contract, date_now):
    #     mysql.add_user(
    #         name='test',
    #         email='test@example.com',
    #         password='password',
    #         employee_number=1,
    #         department_id=1
    #     )
    #     mysql.add_client(
    #         name='Antoine',
    #         email='client@example.com',
    #         phone='0202020202',
    #         entreprise_name='Entreprise 1',
    #         commercial_contact_id=1
    #     )
    #     mysql.add_contract(
    #         client_id=1,
    #         total_amount=1000,
    #         rest_amount=1000
    #     )
    #     mysql.add_event(
    #         contract_id=1,
    #         support_contact_id=1,
    #         location='endroit',
    #         attendees=100,
    #         notes='Ne pas oublier',
    #         date_start=date_now
    #     )
    #     result = mysql.get_event_list_by_client(1)
    #     assert len(result) != 0

    # def test_get_event_list_by_user(self, mysql, empty_contract, date_now):
    #     mysql.add_user(
    #         name='test',
    #         email='test@example.com',
    #         password='password',
    #         employee_number=1,
    #         department_id=1
    #     )
    #     mysql.add_client(
    #         name='Antoine',
    #         email='client@example.com',
    #         phone='0202020202',
    #         entreprise_name='Entreprise 1',
    #         commercial_contact_id=1
    #     )
    #     mysql.add_contract(
    #         client_id=1,
    #         total_amount=1000,
    #         rest_amount=1000
    #     )
    #     mysql.add_event(
    #         contract_id=1,
    #         support_contact_id=1,
    #         location='endroit',
    #         attendees=100,
    #         notes='Ne pas oublier',
    #         date_start=date_now
    #     )
    #     result = mysql.get_event_list_by_user(1)
    #     assert len(result) != 0
