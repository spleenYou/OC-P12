import func


class TestFailed:
    def test_view_client_without_client(self, controller, commercial_user, monkeypatch, capsys):
        func.connect_user(controller, commercial_user, monkeypatch)
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
        func.connect_user(controller, commercial_user, monkeypatch)
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
        func.connect_user(controller, commercial_user, monkeypatch)
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
