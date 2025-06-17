class TestFailed:
    def connect_user(self, controller, user, monkeypatch):
        inputs = iter(
            [
                user['password'],
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.session.new_user = user
        controller.db.add_user()
        controller.session.reset_session()
        controller.session.user['email'] = user['email']
        controller.session.user['password'] = user['password']
        controller.db.update_password_user()
        controller.start(user['email'])

    def test_view_client_without_client(self, controller, commercial_user, monkeypatch, capsys):
        self.connect_user(controller, commercial_user, monkeypatch)
        inputs = iter(
            [
                'VIEW CLIENT',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Aucun client n\'est enregistré' in captured.out

    def test_view_contract_without_contract(self, controller, commercial_user, monkeypatch, capsys):
        self.connect_user(controller, commercial_user, monkeypatch)
        inputs = iter(
            [
                'VIEW CONTRACT',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Aucun contrat n\'est enregistré' in captured.out

    def test_view_event_without_event(self, controller, commercial_user, monkeypatch, capsys):
        self.connect_user(controller, commercial_user, monkeypatch)
        inputs = iter(
            [
                'VIEW EVENT',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Aucun évènement n\'est enregistré' in captured.out
