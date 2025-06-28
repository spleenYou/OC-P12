import re
from controllers.db import Mysql


class TestMysql:
    def add_user(self, db, user):
        db.session.user = user
        db.add('user')
        db.session.reset_session()

    def add_client(self, db, client):
        db.session.client = client
        db.add('client')
        db.session.reset_session()

    def add_contract(self, db, contract):
        db.session.contract = contract
        db.add('contract')
        db.session.reset_session()

    def add_event(self, db, event):
        db.session.event = event
        db.add('event')
        db.session.reset_session()

    def test_init_mysql(self, authentication):
        db = Mysql(None, authentication)
        assert db.engine is not None

    def test_number_of_user_empty(self, mysql):
        assert mysql.number_of('user') == 0

    def test_number_of_user_not_empty(self, mysql, management_user):
        mysql.db_session.add(management_user)
        mysql.db_session.commit()
        assert mysql.number_of('user') == 1

    def test_get_password_stored(self, mysql, management_user):
        self.add_user(mysql, management_user)
        mysql.session.connected_user.email = management_user.email
        mysql.session.connected_user.password = 'password'
        mysql.update_password_user(management_user.email)
        password = mysql.get_user_password(management_user.email)
        assert re.search(
            "[$]{1}argon2id[$]{1}v=19[$]{1}m=65536,t=4,p=1[$]{1}[+.\x00-9a-zA-Z]{22}[$]{1}[+.\x00-9a-zA-Z]{43}",
            password
        ) is not None

    def test_get_password_failed(self, mysql):
        assert mysql.get_user_password('test@test.com') is None

    def test_add_in_db_ok(self, mysql, management_user, monkeypatch, secret):
        new_user = management_user
        monkeypatch.setattr(
            target='controllers.authentication.get_key',
            name=lambda path, key: secret
        )
        result = mysql._add_in_db(new_user)
        assert result == 1

    def test_get_department_list(self, mysql):
        departments = ["Commercial", "Support", "Management"]
        assert mysql.get_department_list() == departments

    def test_update_user(self, mysql, management_user):
        self.add_user(mysql, management_user)
        result = mysql.get_user_by_number(0)
        assert result.name == management_user.name
        result.name = 'Nouveau nom'
        result = mysql.get_user_by_number(0)
        assert result.name == 'Nouveau nom'

    def test_get_user_list(self, mysql, management_user):
        self.add_user(mysql, management_user)
        result = mysql.get_list('user')
        assert len(result) != 0
        assert result[0].name == management_user.name
        assert result[0].email == management_user.email
        assert result[0].employee_number == management_user.employee_number
        assert result[0].department_id == management_user.department_id

    def test_delete_user(self, mysql, management_user):
        self.add_user(mysql, management_user)
        users = mysql.get_list('user')
        assert mysql.number_of('user') == 1
        mysql.session.user = users[0]
        result = mysql.delete('user')
        assert result is True
        assert mysql.number_of('user') == 0

    def test_delete_user_failed(self, mysql):
        assert mysql.delete('user') is False

    def test_add_client(self, mysql, commercial_user):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        mysql.session.client.name = 'Nom du client'
        mysql.session.client.email = 'client@example.com'
        mysql.session.client.phone = '0202020202'
        mysql.session.client.company_name = 'Nom de l\'entreprise du client'
        result = mysql.add('client')
        assert result is True

    def test_update_client(self, mysql, commercial_user, client_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client(0)
        assert mysql.session.client.name == client_information.name
        mysql.session.client.name = 'Nouveau nom'
        client = mysql.get_client(0)
        assert client.name == 'Nouveau nom'

    def test_delete_client(self, mysql, commercial_user, client_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        clients = mysql.get_list('client')
        assert len(clients) == 1
        mysql.session.client = clients[0]
        assert mysql.delete('client') is True
        assert len(mysql.get_list('client')) == 0

    def test_delete_client_failed(self, mysql, commercial_user, client_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        assert len(mysql.get_list('client')) == 1
        assert mysql.delete('client') is False
        assert len(mysql.get_list('client')) == 1

    def test_get_client_list(self, mysql, commercial_user, client_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        clients = mysql.get_list('client')
        assert len(clients) != 0
        assert clients[0].name == client_information.name
        assert clients[0].email == client_information.email
        assert clients[0].company_name == client_information.company_name
        assert clients[0].commercial_contact_id == 1

    def test_add_contract(self, mysql, commercial_user, client_information, contract_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client(0)
        mysql.session.contract = contract_information
        result = mysql.add('contract')
        assert result is True

    def test_update_contract(self, mysql, commercial_user, client_information, contract_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client(0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get_client(0)
        mysql.session.contract = mysql.get_contract(0)
        assert mysql.session.contract.rest_amount == int(contract_information.total_amount)
        mysql.session.contract.rest_amount = 500
        mysql.session.contract = mysql.get_contract(0)
        assert mysql.session.contract.rest_amount == 500

    def test_delete_contract(self, mysql, commercial_user, client_information, contract_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client(0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get_client(0)
        mysql.session.contract = mysql.get_contract(0)
        assert len(mysql.get_list('contract')) == 1
        assert mysql.delete('contract') is True
        assert len(mysql.get_list('contract')) == 0

    def test_delete_contract_failed(self, mysql, commercial_user, client_information, contract_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client(0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get_client(0)
        assert len(mysql.get_list('contract')) == 1
        assert mysql.delete('contract') is False
        assert len(mysql.get_list('contract')) == 1

    def test_get_contract_list(self, mysql, commercial_user, client_information, contract_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client(0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get_client(0)
        result = mysql.get_list('contract')
        assert len(result) != 0
        assert result[0].client_id == mysql.session.client.id
        assert result[0].total_amount == contract_information.total_amount
        assert result[0].rest_amount == contract_information.total_amount

    def test_add_event(
            self,
            mysql,
            commercial_user,
            client_information,
            contract_information,
            event_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client(0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get_client(0)
        mysql.session.contract = mysql.get_contract(0)
        mysql.session.event = event_information
        result = mysql.add('event')
        assert result is True

    def test_update_event(
            self,
            mysql,
            commercial_user,
            client_information,
            contract_information,
            support_user,
            event_information):
        self.add_user(mysql, commercial_user)
        self.add_user(mysql, support_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client(0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get_client(0)
        mysql.session.contract = mysql.get_contract(0)
        self.add_event(mysql, event_information)
        mysql.session.client = mysql.get_client(0)
        mysql.session.contract = mysql.get_contract(0)
        assert mysql.session.contract.event.attendees == event_information.attendees
        mysql.session.contract.event.attendees = 200
        mysql.session.contract = mysql.get_contract(0)
        assert mysql.session.contract.event.attendees == 200

    def test_delete_event(
            self,
            mysql,
            commercial_user,
            client_information,
            contract_information,
            support_user,
            event_information):
        self.add_user(mysql, commercial_user)
        self.add_user(mysql, support_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client(0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get_client(0)
        mysql.session.contract = mysql.get_contract(0)
        self.add_event(mysql, event_information)
        mysql.session.client = mysql.get_client(0)
        mysql.session.contract = mysql.get_contract(0)
        mysql.session.event = mysql.session.contract.event
        assert mysql.session.contract.event is not None
        assert mysql.delete('event') is True
        assert mysql.session.contract.event is None

    def test_delete_event_failed(
            self,
            mysql,
            commercial_user,
            client_information,
            contract_information,
            support_user,
            event_information):
        self.add_user(mysql, commercial_user)
        self.add_user(mysql, support_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client(0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get_client(0)
        mysql.session.contract = mysql.get_contract(0)
        assert mysql.session.contract.event is None
        assert mysql.delete('event') is False

    def test_number_of_contract(
            self,
            mysql,
            commercial_user,
            support_user,
            client_information,
            contract_information):
        self.add_user(mysql, commercial_user)
        self.add_user(mysql, support_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client(0)
        self.add_contract(mysql, contract_information)
        assert mysql.number_of('contract') == 1

    def test_number_of_contract_for_user(
            self,
            mysql,
            commercial_user,
            support_user,
            client_information,
            contract_information):
        self.add_user(mysql, commercial_user)
        self.add_user(mysql, support_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client(0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get_client(0)
        assert mysql.number_of('contract') == 1

    def test_number_of_contract_with_event(
            self,
            mysql,
            commercial_user,
            support_user,
            client_information,
            contract_information):
        self.add_user(mysql, commercial_user)
        self.add_user(mysql, support_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client(0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get_client(0)
        mysql.session.filter = 'WITH_EVENT'
        assert mysql.number_of('contract') == 0

    def test_number_of_contract_without_event(
            self,
            mysql,
            commercial_user,
            support_user,
            client_information,
            contract_information):
        self.add_user(mysql, commercial_user)
        self.add_user(mysql, support_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client(0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get_client(0)
        mysql.session.filter = 'WITHOUT_EVENT'
        assert mysql.number_of('contract') == 1

    def test_number_of_event(
            self,
            mysql,
            commercial_user,
            support_user,
            client_information,
            contract_information,
            event_information):
        self.add_user(mysql, commercial_user)
        self.add_user(mysql, support_user)
        mysql.session.connected_user = mysql.get_user_by_number(0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get_client(0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get_client(0)
        mysql.session.contract = mysql.get_contract(0)
        self.add_event(mysql, event_information)
        assert mysql.number_of('event') == 1

    def test_get_user_by_number(self, mysql, commercial_user):
        self.add_user(mysql, commercial_user)
        assert mysql.get_user_by_number(0).id == 1

    def test_get_user_by_mail(self, mysql, commercial_user):
        self.add_user(mysql, commercial_user)
        assert mysql.get_user_by_mail(commercial_user.email).id == 1
