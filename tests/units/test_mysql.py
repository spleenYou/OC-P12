import re
from controllers.db import Mysql


class TestMysql:
    def add_user(self, db, user):
        db.session.user = user
        db.session.set_session(model='USER')
        db.add()
        db.session.reset_session()

    def add_client(self, db, client):
        db.session.client = client
        db.session.set_session(model='CLIENT')
        db.add()
        db.session.reset_session()

    def add_contract(self, db, contract):
        db.session.contract = contract
        db.session.set_session(model='CONTRACT')
        db.add()
        db.session.reset_session()

    def add_event(self, db, event):
        db.session.event = event
        db.session.set_session(model='EVENT')
        db.add()
        db.session.reset_session()

    def test_init_mysql(self, authentication):
        db = Mysql(None, authentication)
        assert db.engine is not None

    def test_number_of_user_empty(self, mysql):
        assert mysql.number_of('USER') == 0

    def test_number_of_user_not_empty(self, mysql, management_user):
        mysql.db_session.add(management_user)
        mysql.db_session.commit()
        assert mysql.number_of('USER') == 1

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

    def test_get_department_list(self, mysql):
        departments = ["Commercial", "Support", "Management"]
        assert mysql.get_department_list() == departments

    def test_update_user(self, mysql, management_user):
        self.add_user(mysql, management_user)
        result = mysql.get('USER', 0)
        assert result.name == management_user.name
        result.name = 'Nouveau nom'
        mysql.db_session.commit()
        result = mysql.get('USER', 0)
        assert result.name == 'Nouveau nom'

    def test_get_user_list(self, mysql, management_user):
        self.add_user(mysql, management_user)
        result = mysql.get_list('USER')
        assert len(result) != 0
        assert result[0].name == management_user.name
        assert result[0].email == management_user.email
        assert result[0].employee_number == management_user.employee_number
        assert result[0].department_id == management_user.department_id

    def test_delete_user(self, mysql, management_user):
        self.add_user(mysql, management_user)
        mysql.session.set_session(model='USER')
        users = mysql.get_list('USER')
        assert mysql.number_of('USER') == 1
        mysql.session.user = users[0]
        result = mysql.delete()
        assert result is True
        assert mysql.number_of('USER') == 0

    def test_delete_user_failed(self, mysql):
        mysql.session.set_session(model='USER')
        assert mysql.delete() is False

    def test_add_client(self, mysql, commercial_user):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get('USER', 0)
        mysql.session.client.name = 'Nom du client'
        mysql.session.client.email = 'client@example.com'
        mysql.session.client.phone = '0202020202'
        mysql.session.client.company_name = 'Nom de l\'entreprise du client'
        mysql.session.set_session(model='CLIENT')
        result = mysql.add()
        assert result is True

    def test_update_client(self, mysql, commercial_user, client_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        assert mysql.session.client.name == client_information.name
        mysql.session.client.name = 'Nouveau nom'
        mysql.db_session.commit()
        client = mysql.get('CLIENT', 0)
        assert client.name == 'Nouveau nom'

    def test_delete_client(self, mysql, commercial_user, client_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        clients = mysql.get_list('CLIENT')
        assert len(clients) == 1
        mysql.session.client = clients[0]
        mysql.session.set_session(model='CLIENT')
        assert mysql.delete() is True
        assert len(mysql.get_list('CLIENT')) == 0

    def test_delete_client_failed(self, mysql, commercial_user, client_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        assert len(mysql.get_list('CLIENT')) == 1
        mysql.session.set_session(model='CLIENT')
        assert mysql.delete() is False
        assert len(mysql.get_list('CLIENT')) == 1

    def test_get_client_list(self, mysql, commercial_user, client_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        clients = mysql.get_list('CLIENT')
        assert len(clients) != 0
        assert clients[0].name == client_information.name
        assert clients[0].email == client_information.email
        assert clients[0].company_name == client_information.company_name
        assert clients[0].commercial_contact_id == 1

    def test_add_contract(self, mysql, commercial_user, client_information, contract_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        mysql.session.contract = contract_information
        mysql.session.set_session(model='CONTRACT')
        result = mysql.add()
        assert result is True

    def test_update_contract(self, mysql, commercial_user, client_information, contract_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        mysql.session.contract = mysql.get('CONTRACT', 0)
        assert mysql.session.contract.rest_amount == int(contract_information.total_amount)
        mysql.session.contract.rest_amount = 500
        mysql.db_session.commit()
        mysql.session.contract = mysql.get('CONTRACT', 0)
        assert mysql.session.contract.rest_amount == 500

    def test_delete_contract(self, mysql, commercial_user, client_information, contract_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        mysql.session.contract = mysql.get('CONTRACT', 0)
        assert len(mysql.get_list('CONTRACT')) == 1
        mysql.session.set_session(model='CONTRACT')
        assert mysql.delete() is True
        assert len(mysql.get_list('CONTRACT')) == 0

    def test_delete_contract_failed(self, mysql, commercial_user, client_information, contract_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        assert len(mysql.get_list('CONTRACT')) == 1
        mysql.session.set_session(model='CONTRACT')
        assert mysql.delete() is False
        assert len(mysql.get_list('CONTRACT')) == 1

    def test_get_contract_list(self, mysql, commercial_user, client_information, contract_information):
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        result = mysql.get_list('CONTRACT')
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
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        mysql.session.contract = mysql.get('CONTRACT', 0)
        mysql.session.event = event_information
        mysql.session.set_session(model='EVENT')
        result = mysql.add()
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
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        mysql.session.contract = mysql.get('CONTRACT', 0)
        self.add_event(mysql, event_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        mysql.session.contract = mysql.get('CONTRACT', 0)
        assert mysql.session.contract.event.attendees == event_information.attendees
        mysql.session.contract.event.attendees = 200
        mysql.db_session.commit()
        mysql.session.contract = mysql.get('CONTRACT', 0)
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
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        mysql.session.contract = mysql.get('CONTRACT', 0)
        self.add_event(mysql, event_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        mysql.session.contract = mysql.get('CONTRACT', 0)
        mysql.session.event = mysql.session.contract.event
        assert mysql.session.contract.event is not None
        mysql.session.set_session(model='EVENT')
        assert mysql.delete() is True
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
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        mysql.session.contract = mysql.get('CONTRACT', 0)
        assert mysql.session.contract.event is None
        mysql.session.set_session(model='EVENT')
        assert mysql.delete() is False

    def test_number_of_contract(
            self,
            mysql,
            commercial_user,
            support_user,
            client_information,
            contract_information):
        self.add_user(mysql, commercial_user)
        self.add_user(mysql, support_user)
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        self.add_contract(mysql, contract_information)
        assert mysql.number_of('CONTRACT') == 1

    def test_number_of_contract_for_user(
            self,
            mysql,
            commercial_user,
            support_user,
            client_information,
            contract_information):
        self.add_user(mysql, commercial_user)
        self.add_user(mysql, support_user)
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        assert mysql.number_of('CONTRACT') == 1

    def test_number_of_contract_with_event(
            self,
            mysql,
            commercial_user,
            support_user,
            client_information,
            contract_information):
        self.add_user(mysql, commercial_user)
        self.add_user(mysql, support_user)
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        mysql.session.filter = 'WITH_EVENT'
        assert mysql.number_of('CONTRACT') == 0

    def test_number_of_contract_without_event(
            self,
            mysql,
            commercial_user,
            support_user,
            client_information,
            contract_information):
        self.add_user(mysql, commercial_user)
        self.add_user(mysql, support_user)
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        mysql.session.filter = 'WITHOUT_EVENT'
        assert mysql.number_of('CONTRACT') == 1

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
        mysql.session.connected_user = mysql.get('USER', 0)
        self.add_client(mysql, client_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        self.add_contract(mysql, contract_information)
        mysql.session.client = mysql.get('CLIENT', 0)
        mysql.session.contract = mysql.get('CONTRACT', 0)
        self.add_event(mysql, event_information)
        assert mysql.number_of('EVENT') == 1

    def test_get_user_by_number(self, mysql, commercial_user):
        self.add_user(mysql, commercial_user)
        assert mysql.get('USER', 0).id == 1

    def test_get_user_by_mail(self, mysql, commercial_user):
        mysql.session.set_session(filter='EMAIL')
        self.add_user(mysql, commercial_user)
        mysql.session.connected_user.email = commercial_user.email
        assert mysql.get('USER', 0).id == 1
