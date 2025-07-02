import pytest
import func


class TestSupport:
    @pytest.fixture(autouse=True)
    def setup(self, controller, support_user, monkeypatch):
        func.connect_user(controller, support_user, monkeypatch)

    def test_add_user(self, controller, support_user, monkeypatch, capsys):
        inputs = iter(
            [
                'ADD USER',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_update_user(self, controller, support_user, monkeypatch, capsys):
        inputs = iter(
            [
                'UPDATE USER',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_delete_user(self, controller, support_user, monkeypatch, capsys):
        inputs = iter(
            [
                'DELETE USER',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_view_user(self, controller, support_user, monkeypatch, capsys):
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
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Sélection d\'un utilisateur' in captured.out
        assert 'Informations sur l\'utilisateur' in captured.out

    def test_add_client(self, controller, support_user, monkeypatch, capsys):
        inputs = iter(
            [
                'ADD CLIENT',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_update_client(self, controller, support_user, client_information, monkeypatch, capsys):
        func.add_client(controller, client_information)
        inputs = iter(
            [
                'UPDATE CLIENT',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_delete_client(self, controller, support_user, client_information, monkeypatch, capsys):
        func.add_client(controller, client_information)
        inputs = iter(
            [
                'DELETE CLIENT',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_view_client(self, controller, support_user, client_information, monkeypatch, capsys):
        func.add_client(controller, client_information)
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
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Informations sur le client' in captured.out
        assert client_information.name in captured.out

    def test_add_contract(
            self,
            controller,
            support_user,
            client_information,
            monkeypatch,
            capsys):
        func.add_client(controller, client_information)
        inputs = iter(
            [
                'ADD CONTRACT',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_update_contract(
            self,
            controller,
            support_user,
            client_information,
            contract_information,
            monkeypatch,
            capsys):
        func.add_client(controller, client_information)
        func.add_contract(controller, contract_information, 0)
        inputs = iter(
            [
                'UPDATE CONTRACT',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_delete_contract(
            self,
            controller,
            support_user,
            client_information,
            contract_information,
            monkeypatch,
            capsys):
        func.add_client(controller, client_information)
        func.add_contract(controller, contract_information, 0)
        inputs = iter(
            [
                'DELETE CONTRACT',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_view_contract(
            self,
            controller,
            support_user,
            client_information,
            contract_information,
            monkeypatch,
            capsys):
        func.add_client(controller, client_information)
        func.add_contract(controller, contract_information, 0)
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
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Informations sur le contrat' in captured.out

    def test_add_event(
            self,
            controller,
            commercial_user,
            support_user,
            client_information,
            contract_information,
            monkeypatch,
            capsys):
        func.add_user(controller, commercial_user)
        func.add_client(controller, client_information)
        func.add_contract(controller, contract_information, 0)
        inputs = iter(
            [
                'ADD EVENT',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_update_event(
            self,
            controller,
            commercial_user,
            support_user,
            client_information,
            contract_information,
            event_information,
            monkeypatch,
            capsys):
        func.add_user(controller, commercial_user)
        func.add_client(controller, client_information)
        func.add_contract(controller, contract_information, 0)
        func.add_event(controller, event_information, 0, 1, 0)
        inputs = iter(
            [
                'UPDATE EVENT',
                '0',
                '0',
                'Pas loin',
                '',
                '',
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
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        for c in captured:
            print(c)
        assert 'Mise à jour d\'un évènement' in captured.out
        assert 'Pas loin' in captured.out
        assert 'Evènement mis à jour' in captured.out

    def test_delete_event(
            self,
            controller,
            commercial_user,
            support_user,
            client_information,
            contract_information,
            event_information,
            monkeypatch,
            capsys):
        func.add_user(controller, commercial_user)
        func.add_client(controller, client_information)
        func.add_contract(controller, contract_information, 0)
        func.add_event(controller, event_information, 0, 1, 0)
        inputs = iter(
            [
                'DELETE EVENT',
                '0',
                '0',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Suppression d\'un évènement' in captured.out
        assert 'Evènement supprimé' in captured.out

    def test_view_event(
            self,
            controller,
            commercial_user,
            support_user,
            client_information,
            contract_information,
            event_information,
            monkeypatch,
            capsys):
        func.add_user(controller, commercial_user)
        func.add_client(controller, client_information)
        func.add_contract(controller, contract_information, 0)
        func.add_event(controller, event_information, 0, 1, 0)
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
        with pytest.raises(SystemExit):
            controller.main_menu()
        captured = capsys.readouterr()
        assert 'Informations sur l\'évènement' in captured.out
