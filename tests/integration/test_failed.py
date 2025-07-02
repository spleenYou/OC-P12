import pytest
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
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        for c in captured:
            print(c)
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
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Cette action sur les contrats n\'est pas possible pour le moment' in captured.out

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
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Cette action sur les évènements n\'est pas possible pour le moment' in captured.out

    def test_command_with_wrong_token(self, controller, monkeypatch, management_user, capsys, commercial_user):
        func.add_user(controller, management_user)
        func.connect_user(controller, management_user, monkeypatch)
        controller.session.token = 'wrong token'
        inputs = iter(
            [
                'ADD USER',
                '',
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Déconnexion automatique' in captured.out
        assert 'Vous avez été déconnecté, merci de vous reconnecter' in captured.out
