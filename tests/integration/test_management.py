import pytest
import func


class TestManagement:
    @pytest.fixture(autouse=True)
    def setup(self, controller, management_user, monkeypatch):
        func.connect_user(controller, management_user, monkeypatch)

    def test_add_user(self, controller, management_user, commercial_user, monkeypatch, capsys):
        inputs = iter(
            [
                'ADD USER',
                commercial_user.name,
                commercial_user.email,
                commercial_user.employee_number,
                commercial_user.department_id,
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
        func.add_user(controller, commercial_user)
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
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_delete_client(self, controller, management_user, client_information, monkeypatch, capsys):
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
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_view_client(self, controller, management_user, client_information, monkeypatch, capsys):
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
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Informations sur le client' in captured.out
        assert client_information.name in captured.out

    def test_add_contract(
            self,
            controller,
            management_user,
            client_information,
            contract_information,
            monkeypatch,
            capsys):
        func.add_client(controller, client_information)
        inputs = iter(
            [
                'ADD CONTRACT',
                '0',
                contract_information.total_amount,
                contract_information.total_amount,
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
        func.add_user(controller, commercial_user)
        func.add_client(controller, client_information)
        func.add_contract(controller, contract_information, 0)
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
        func.add_user(controller, commercial_user)
        func.add_client(controller, client_information)
        func.add_contract(controller, contract_information, 0)
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
        func.add_user(controller, commercial_user)
        func.add_client(controller, client_information)
        func.add_contract(controller, contract_information, 0)
        func.add_event(controller, event_information, 0, 1, 0)
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
        func.add_user(controller, commercial_user)
        func.add_client(controller, client_information)
        func.add_contract(controller, contract_information, 0)
        func.add_event(controller, event_information, 0, 1, 0)
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
        func.add_user(controller, support_user)
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
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Informations sur l\'évènement' in captured.out
