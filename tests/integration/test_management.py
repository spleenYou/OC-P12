class TestManagement:
    def connect_user(self, controller, management_user, monkeypatch):
        inputs = iter(
            [
                management_user['password'],
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.session.new_user = management_user
        controller.db.add_user()
        controller.session.reset_session()
        controller.session.user['email'] = management_user['email']
        controller.session.user['password'] = management_user['password']
        controller.db.update_password_user()
        controller.start(management_user['email'])

    def add_client(self, controller, client):
        controller.session.client = client
        controller.db.add_client()
        controller.session.client = {
            'id': None,
            'name': None,
            'email': None,
            'phone': None,
            'company_name': None,
            'commercial_contact_id': None
        }

    def add_user(self, controller, user):
        controller.session.new_user = user
        controller.db.add_user()
        controller.session.new_user = {
            'id': None,
            'name': None,
            'email': None,
            'password': None,
            'employee_number': None,
            'department_id': None
        }

    def add_contract(self, controller, contract, client_id):
        controller.session.client = controller.db.get_client_information(client_id)
        controller.session.contract = contract
        controller.db.add_contract()
        controller.session.contract = {
            'id': None,
            'client_id': None,
            'total_amount': None,
            'rest_amount': None,
            'status': False
        }

    def add_event(self, controller, event, contract_id, support_user_id):
        event['support_contact_id'] = support_user_id
        controller.session.contract = controller.db.get_contract_information(contract_id)
        controller.session.event = event
        controller.db.add_event()
        controller.session.event = {
            'id': None,
            'support_contact_id': None,
            'location': None,
            'attendees': None,
            'notes': None,
            'date_start': None,
            'date_stop': None
        }

    def test_add_user(self, controller, management_user, commercial_user, monkeypatch, capsys):
        self.connect_user(controller, management_user, monkeypatch)
        inputs = iter(
            [
                'ADD USER',
                commercial_user['name'],
                commercial_user['email'],
                commercial_user['employee_number'],
                commercial_user['department_id'],
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Ajout d\'un utilisateur' in captured.out
        assert 'Utilisateur créé' in captured.out

    def test_update_user(self, controller, management_user, monkeypatch, capsys):
        self.connect_user(controller, management_user, monkeypatch)
        inputs = iter(
            [
                'UPDATE USER',
                '0',
                '',
                'new_email@example.com',
                '',
                '',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Mise à jour d\'un utilisateur' in captured.out
        assert 'Utilisateur mis à jour' in captured.out

    def test_delete_user(self, controller, management_user, commercial_user, monkeypatch, capsys):
        self.connect_user(controller, management_user, monkeypatch)
        self.add_user(controller, commercial_user)
        inputs = iter(
            [
                'DELETE USER',
                '0',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Suppression d\'un utilisateur' in captured.out
        assert 'Utilisateur supprimé' in captured.out

    def test_view_user(self, controller, management_user, monkeypatch, capsys):
        self.connect_user(controller, management_user, monkeypatch)
        inputs = iter(
            [
                'VIEW USER',
                '0',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Sélection d\'un utilisateur' in captured.out
        assert 'Informations sur l\'utilisateur' in captured.out

    def test_add_client(self, controller, management_user, monkeypatch, capsys):
        self.connect_user(controller, management_user, monkeypatch)
        inputs = iter(
            [
                'ADD CLIENT',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_update_client(self, controller, management_user, client_information, monkeypatch, capsys):
        self.connect_user(controller, management_user, monkeypatch)
        self.add_client(controller, client_information)
        inputs = iter(
            [
                'UPDATE CLIENT',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_delete_client(self, controller, management_user, client_information, monkeypatch, capsys):
        self.connect_user(controller, management_user, monkeypatch)
        self.add_client(controller, client_information)
        inputs = iter(
            [
                'DELETE CLIENT',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_view_client(self, controller, management_user, client_information, monkeypatch, capsys):
        self.connect_user(controller, management_user, monkeypatch)
        self.add_client(controller, client_information)
        inputs = iter(
            [
                'VIEW CLIENT',
                '0',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Informations sur le client' in captured.out
        assert client_information['name'] in captured.out

    def test_add_contract(
            self,
            controller,
            management_user,
            client_information,
            contract_information,
            monkeypatch,
            capsys):
        self.connect_user(controller, management_user, monkeypatch)
        self.add_client(controller, client_information)
        inputs = iter(
            [
                'ADD CONTRACT',
                '0',
                contract_information['total_amount'],
                contract_information['total_amount'],
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Ajout d\'un contrat' in captured.out
        assert 'Contrat ajouté' in captured.out

    def test_update_contract(
            self,
            controller,
            commercial_user,
            management_user,
            client_information,
            contract_information,
            monkeypatch,
            capsys):
        self.add_user(controller, commercial_user)
        self.connect_user(controller, management_user, monkeypatch)
        self.add_client(controller, client_information)
        self.add_contract(controller, contract_information, 1)
        inputs = iter(
            [
                'UPDATE CONTRACT',
                '0',
                '0',
                '',
                '',
                '',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Mise à jour d\'un contrat' in captured.out
        assert 'Contrat mis à jour' in captured.out

    def test_delete_contract(
            self,
            controller,
            commercial_user,
            management_user,
            client_information,
            contract_information,
            monkeypatch,
            capsys):
        self.add_user(controller, commercial_user)
        self.connect_user(controller, management_user, monkeypatch)
        self.add_client(controller, client_information)
        self.add_contract(controller, contract_information, 1)
        inputs = iter(
            [
                'DELETE CONTRACT',
                '0',
                '0',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Suppression d\'un contrat' in captured.out
        assert 'Contrat supprimé' in captured.out

    def test_view_contract(
            self,
            controller,
            management_user,
            client_information,
            contract_information,
            monkeypatch,
            capsys):
        self.connect_user(controller, management_user, monkeypatch)
        self.add_client(controller, client_information)
        self.add_contract(controller, contract_information, 1)
        inputs = iter(
            [
                'VIEW CONTRACT',
                '0',
                '0',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Informations sur le contrat' in captured.out

    def test_add_event(
            self,
            controller,
            management_user,
            commercial_user,
            client_information,
            contract_information,
            event_information,
            monkeypatch,
            capsys):
        self.add_user(controller, commercial_user)
        self.connect_user(controller, management_user, monkeypatch)
        self.add_client(controller, client_information)
        self.add_contract(controller, contract_information, 1)
        inputs = iter(
            [
                'ADD EVENT',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_update_event(
            self,
            controller,
            management_user,
            commercial_user,
            client_information,
            contract_information,
            event_information,
            monkeypatch,
            capsys):
        self.add_user(controller, commercial_user)
        self.connect_user(controller, management_user, monkeypatch)
        self.add_client(controller, client_information)
        self.add_contract(controller, contract_information, 1)
        self.add_event(controller, event_information, 1, 1)
        inputs = iter(
            [
                'UPDATE EVENT',
                '0',
                '0',
                '',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Evènement mis à jour' in captured.out

    def test_delete_event(
            self,
            controller,
            management_user,
            commercial_user,
            client_information,
            contract_information,
            event_information,
            monkeypatch,
            capsys):
        self.add_user(controller, commercial_user)
        self.connect_user(controller, management_user, monkeypatch)
        self.add_client(controller, client_information)
        self.add_contract(controller, contract_information, 1)
        self.add_event(controller, event_information, 1, 1)
        inputs = iter(
            [
                'DELETE EVENT',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_view_event(
            self,
            controller,
            management_user,
            support_user,
            client_information,
            contract_information,
            event_information,
            monkeypatch,
            capsys):
        self.add_user(controller, support_user)
        self.connect_user(controller, management_user, monkeypatch)
        self.add_client(controller, client_information)
        self.add_contract(controller, contract_information, 1)
        self.add_event(controller, event_information, 1, 1)
        inputs = iter(
            [
                'VIEW EVENT',
                '0',
                '0',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Informations sur l\'évènement' in captured.out
