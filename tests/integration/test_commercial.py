class TestCommercial:
    def connect_user(self, controller, commercial_user, monkeypatch):
        inputs = iter(
            [
                commercial_user['password'],
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.session.new_user = commercial_user
        controller.db.add_user()
        controller.session.reset_session()
        controller.session.user['email'] = commercial_user['email']
        controller.session.user['password'] = commercial_user['password']
        controller.db.update_password_user()
        controller.start(commercial_user['email'])

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

    def add_contract(self, controller, contract, client_id):
        controller.session.client = controller.db.get_client_information(client_id)
        controller.session.contract = contract
        controller.db.add_contract()
        controller.session.reset_session()

    def add_event(self, controller, event, contract_id, support_user_id):
        event['support_contact_id'] = support_user_id
        controller.session.contract = controller.db.get_contract_information(contract_id)
        controller.session.event = event
        controller.db.add_event()
        controller.session.reset_session()

    def test_add_user(self, controller, commercial_user, monkeypatch, capsys):
        self.connect_user(controller, commercial_user, monkeypatch)
        inputs = iter(
            [
                'ADD USER',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_update_user(self, controller, commercial_user, monkeypatch, capsys):
        self.connect_user(controller, commercial_user, monkeypatch)
        inputs = iter(
            [
                'UPDATE USER',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_delete_user(self, controller, commercial_user, monkeypatch, capsys):
        self.connect_user(controller, commercial_user, monkeypatch)
        inputs = iter(
            [
                'DELETE USER',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_view_user(self, controller, commercial_user, monkeypatch, capsys):
        self.connect_user(controller, commercial_user, monkeypatch)
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

    def test_add_client(self, controller, commercial_user, client_information, monkeypatch, capsys):
        self.connect_user(controller, commercial_user, monkeypatch)
        inputs = iter(
            [
                'ADD CLIENT',
                client_information['company_name'],
                client_information['name'],
                client_information['email'],
                client_information['phone'],
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Ajout d\'un client' in captured.out
        assert 'Client ajouté' in captured.out

    def test_update_client(self, controller, commercial_user, client_information, monkeypatch, capsys):
        self.connect_user(controller, commercial_user, monkeypatch)
        self.add_client(controller, client_information)
        inputs = iter(
            [
                'UPDATE CLIENT',
                '0',
                '',
                client_information['name'] + '2',
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
        assert 'Mise à jour d\'un client' in captured.out
        assert client_information['name'] + '2' in captured.out
        assert 'Client mis à jour' in captured.out

    def test_delete_client(self, controller, commercial_user, client_information, monkeypatch, capsys):
        self.connect_user(controller, commercial_user, monkeypatch)
        self.add_client(controller, client_information)
        inputs = iter(
            [
                'DELETE CLIENT',
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
        assert 'Suppression d\'un client' in captured.out
        assert 'Client supprimé' in captured.out

    def test_view_client(self, controller, commercial_user, client_information, monkeypatch, capsys):
        self.connect_user(controller, commercial_user, monkeypatch)
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
