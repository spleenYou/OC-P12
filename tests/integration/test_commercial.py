import func


class TestCommercial:
    def test_add_user(self, controller, commercial_user, monkeypatch, capsys):
        func.connect_user(controller, commercial_user, monkeypatch)
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
        func.connect_user(controller, commercial_user, monkeypatch)
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
        func.connect_user(controller, commercial_user, monkeypatch)
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
        func.connect_user(controller, commercial_user, monkeypatch)
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
        func.connect_user(controller, commercial_user, monkeypatch)
        inputs = iter(
            [
                'ADD CLIENT',
                client_information.company_name,
                client_information.name,
                client_information.email,
                client_information.phone,
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
        func.connect_user(controller, commercial_user, monkeypatch)
        func.add_client(controller, client_information)
        inputs = iter(
            [
                'UPDATE CLIENT',
                '0',
                '',
                client_information.name + '2',
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
        assert client_information.name in captured.out
        assert 'Client mis à jour' in captured.out

    def test_delete_client(self, controller, commercial_user, client_information, monkeypatch, capsys):
        func.connect_user(controller, commercial_user, monkeypatch)
        func.add_client(controller, client_information)
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
        func.connect_user(controller, commercial_user, monkeypatch)
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
            commercial_user,
            client_information,
            monkeypatch,
            capsys):
        func.connect_user(controller, commercial_user, monkeypatch)
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
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_update_contract_without_change(
            self,
            controller,
            commercial_user,
            client_information,
            contract_information,
            monkeypatch,
            capsys):
        func.connect_user(controller, commercial_user, monkeypatch)
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
        for c in captured:
            print(c)
        assert 'Mise à jour d\'un contrat' in captured.out
        assert 'Contrat mis à jour' in captured.out

    def test_update_contract_with_change(
            self,
            controller,
            commercial_user,
            client_information,
            contract_information,
            monkeypatch,
            capsys):
        func.connect_user(controller, commercial_user, monkeypatch)
        func.add_client(controller, client_information)
        func.add_contract(controller, contract_information, 0)
        inputs = iter(
            [
                'UPDATE CONTRACT',
                '0',
                '0',
                '10',
                '10',
                'n',
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
            client_information,
            contract_information,
            monkeypatch,
            capsys):
        func.connect_user(controller, commercial_user, monkeypatch)
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
            commercial_user,
            client_information,
            contract_information,
            monkeypatch,
            capsys):
        func.connect_user(controller, commercial_user, monkeypatch)
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
            commercial_user,
            support_user,
            client_information,
            contract_information,
            event_information,
            monkeypatch,
            capsys):
        func.connect_user(controller, support_user, monkeypatch)
        func.connect_user(controller, commercial_user, monkeypatch)
        func.add_client(controller, client_information)
        func.add_contract(controller, contract_information, 0)
        inputs = iter(
            [
                'ADD EVENT',
                '0',
                '0',
                event_information.location,
                event_information.attendees,
                event_information.date_start.strftime('%d/%m/%Y'),
                event_information.date_stop.strftime('%d/%m/%Y'),
                event_information.notes,
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
        assert 'Ajout d\'un évènement' in captured.out
        assert 'Evènement ajouté' in captured.out

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
        func.connect_user(controller, support_user, monkeypatch)
        func.connect_user(controller, commercial_user, monkeypatch)
        func.add_client(controller, client_information)
        func.add_contract(controller, contract_information, 0)
        func.add_event(controller, event_information, 0, 1, 0)
        inputs = iter(
            [
                'UPDATE EVENT',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

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
        func.connect_user(controller, support_user, monkeypatch)
        func.connect_user(controller, commercial_user, monkeypatch)
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
        func.connect_user(controller, support_user, monkeypatch)
        func.connect_user(controller, commercial_user, monkeypatch)
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
