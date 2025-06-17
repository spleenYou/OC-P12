from controllers.base import Controller
from controllers.authentication import Authentication
from controllers.db import Mysql
from views.prompt import Ask
from views.show import Show


class TestController:
    def test_init_controller(session):
        ctrl = Controller(Ask, Show, Mysql, Authentication, session)
        assert ctrl.session == session

    def add_user(self, controller, user):
        controller.session.new_user = user
        controller.db.add_user()
        controller.session.reset_session()

    def add_client(self, controller, client):
        controller.session.client = client
        controller.db.add_client()
        controller.session.reset_session()

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

    def connect_user(self, controller, user_id):
        controller.session.user = controller.db.get_user_information(user_id)
        controller.auth.generate_token()

    def test_start_without_user_and_no_registration(self, monkeypatch, controller, management_user, capsys):
        inputs = iter([
            '',
            management_user['name'],
            management_user['email'],
            management_user['employee_number'],
            ''
        ])
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: False)
        controller.start(None)
        captured = capsys.readouterr()
        assert 'Premier lancement de l\'application' in captured.out
        assert 'Utilisateur non enregistré' in captured.out

    def test_login_first_time(self, monkeypatch, controller, management_user, capsys):
        self.add_user(controller, management_user)
        inputs = iter(
            [
                management_user['email'],
                management_user['password'],
                management_user['password'],
                management_user['password'],
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.start(None)
        captured = capsys.readouterr()
        assert 'Définition du mot de passe' in captured.out
        assert 'Veuillez définir votre mot de passe' in captured.out
        assert 'Veuillez entrer une deuxième fois votre mot de passe' in captured.out
        assert 'Connexion réussie' in captured.out

    def test_start_with_user_and_login_failed(self, monkeypatch, controller, management_user, capsys):
        controller.session.new_user = management_user
        controller.db.add_user()
        controller.session.user = controller.db.get_user_information(1)
        inputs = iter(
            [
                management_user['email'],
                management_user['password'],
                management_user['password'],
                management_user['password'] + 'e',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.start(None)
        captured = capsys.readouterr()
        assert 'Erreur de connexion' in captured.out
        assert 'Vos identifiants sont inconnus' in captured.out

    def test_main_menu(self, controller, monkeypatch, management_user, capsys):
        self.add_user(controller, management_user)
        self.connect_user(controller, 1)
        inputs = iter(
            [
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Menu principal' in captured.out
        assert 'Merci d\'entrer la commande correspondant à ce que vous souhaitez faire' in captured.out
        assert 'Entrer "HELP" pour avoir la description des commandes' in captured.out
        assert 'Entrer "EXIT" pour quitter l\'application' in captured.out

    def test_unknown_command(self, controller, monkeypatch, management_user, capsys):
        self.add_user(controller, management_user)
        self.connect_user(controller, 1)
        inputs = iter(
            [
                'unknown',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Erreur de saisie' in captured.out
        assert 'Cette commande est inconnue, veuillez recommencer' in captured.out

    def test_forbidden_command(self, controller, monkeypatch, management_user, capsys):
        self.add_user(controller, management_user)
        self.connect_user(controller, 1)
        inputs = iter(
            [
                'add client',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Vous n\'êtes pas autorisé à faire cette action' in captured.out

    def test_exit_command(self, controller, monkeypatch, management_user, capsys):
        self.add_user(controller, management_user)
        self.connect_user(controller, 1)
        inputs = iter(
            [
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Au revoir' in captured.out

    def test_help(self, controller, monkeypatch, management_user, capsys):
        self.add_user(controller, management_user)
        self.connect_user(controller, 1)
        inputs = iter(
            [
                'HELP',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Aide' in captured.out
        assert 'Liste des actions possibles :' in captured.out
        assert 'ADD | UPDATE | VIEW | DELETE' in captured.out
        assert 'Liste des catégories possibles :' in captured.out
        assert 'USER | CLIENT | CONTRACT | EVENT' in captured.out
        assert 'Syntaxe : ACTION CATEGORIE' in captured.out

    def test_permission(self, controller, monkeypatch, management_user, capsys):
        self.add_user(controller, management_user)
        self.connect_user(controller, 1)
        inputs = iter(
            [
                'PERMISSION',
                '',
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Tableau des permissions' in captured.out

    def test_add_user(self, controller, monkeypatch, management_user, capsys, commercial_user):
        self.add_user(controller, management_user)
        self.connect_user(controller, 1)
        controller.session.status = 'ADD_USER'
        inputs = iter(
            [
                commercial_user['name'],
                commercial_user['email'],
                commercial_user['employee_number'],
                commercial_user['department_id'],
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.add_user()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Utilisateur créé' in captured.out

    def test_update_user(self, controller, monkeypatch, management_user, capsys, commercial_user):
        self.add_user(controller, management_user)
        self.connect_user(controller, 1)
        self.add_user(controller, commercial_user)
        controller.session.status = 'UPDATE_USER'
        inputs = iter(
            [
                1,
                'Commercial 2',
                '',
                '',
                '',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.update_user()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Commercial 2' in captured.out
        assert 'Utilisateur modifié' in captured.out

    def test_delete_user(self, controller, monkeypatch, management_user, capsys, commercial_user):
        self.add_user(controller, management_user)
        self.connect_user(controller, 1)
        self.add_user(controller, commercial_user)
        controller.session.status = 'DELETE_USER'
        inputs = iter(
            [
                '0',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.delete_user()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Utilisateur supprimé' in captured.out

    def test_view_user(self, controller, monkeypatch, management_user, capsys, commercial_user):
        self.add_user(controller, management_user)
        self.connect_user(controller, 1)
        self.add_user(controller, commercial_user)
        controller.session.status = 'VIEW_USER'
        monkeypatch.setattr('builtins.input', lambda *args: '1')
        controller.view_user()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Informations sur l\'utilisateur' in captured.out

    def test_add_client(self, controller, monkeypatch, capsys, commercial_user, client_information):
        self.add_user(controller, commercial_user)
        self.connect_user(controller, 1)
        controller.session.status = 'ADD_CLIENT'
        inputs = iter(
            [
                client_information['company_name'],
                client_information['name'],
                client_information['email'],
                '0502020202',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.add_client()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Client ajouté' in captured.out

    def test_update_client(self, controller, monkeypatch, capsys, commercial_user, client_information):
        self.add_user(controller, commercial_user)
        self.connect_user(controller, 1)
        self.add_client(controller, client_information)
        controller.session.status = 'UPDATE_CLIENT'
        inputs = iter(
            [
                '0',
                'Nouvelle entreprise',
                '',
                '',
                '',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.update_client()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Nouvelle entreprise' in captured.out
        assert 'Client mis à jour' in captured.out

    def test_delete_client(self, controller, monkeypatch, capsys, commercial_user, client_information):
        self.add_user(controller, commercial_user)
        self.connect_user(controller, 1)
        self.add_client(controller, client_information)
        controller.session.status = 'DELETE_CLIENT'
        inputs = iter(
            [
                '0',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.delete_client()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Client supprimé' in captured.out

    def test_view_client(self, controller, monkeypatch, capsys, commercial_user, client_information):
        self.add_user(controller, commercial_user)
        self.connect_user(controller, 1)
        self.add_client(controller, client_information)
        controller.session.status = 'VIEW_CLIENT'
        monkeypatch.setattr('builtins.input', lambda *args: '0')
        controller.view_client()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Informations sur le client' in captured.out

    def test_add_contract(
            self,
            controller,
            monkeypatch,
            capsys,
            management_user,
            client_information,
            contract_information):
        self.add_user(controller, management_user)
        self.connect_user(controller, 1)
        self.add_client(controller, client_information)
        controller.session.status = 'ADD_CONTRACT'
        inputs = iter(
            [
                '0',
                contract_information['total_amount'],
                contract_information['total_amount'],
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.add_contract()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Ajout d\'un contrat' in captured.out

    def test_update_contract(
            self,
            controller,
            monkeypatch,
            capsys,
            commercial_user,
            client_information,
            contract_information):
        self.add_user(controller, commercial_user)
        self.connect_user(controller, 1)
        self.add_client(controller, client_information)
        self.add_contract(controller, contract_information, 1)
        controller.session.status = 'UPDATE_CONTRACT'
        inputs = iter(
            [
                '0',
                '0',
                '',
                '0',
                'y',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.update_contract()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Terminé' in captured.out
        assert 'Contrat mis à jour' in captured.out

    def test_delete_contract(
            self,
            controller,
            monkeypatch,
            capsys,
            commercial_user,
            client_information,
            contract_information):
        self.add_user(controller, commercial_user)
        self.connect_user(controller, 1)
        self.add_client(controller, client_information)
        self.add_contract(controller, contract_information, 1)
        controller.session.status = 'DELETE_CONTRACT'
        inputs = iter(
            [
                '0',
                '0',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.delete_contract()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Contrat supprimé' in captured.out

    def test_view_contract(
            self,
            controller,
            monkeypatch,
            capsys,
            commercial_user,
            client_information,
            contract_information):
        self.add_user(controller, commercial_user)
        self.connect_user(controller, 1)
        self.add_client(controller, client_information)
        self.add_contract(controller, contract_information, 1)
        controller.session.status = 'VIEW_CONTRACT'
        inputs = iter(['0', '0'])
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.view_contract()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Informations sur le contrat' in captured.out

    def test_add_event(
            self,
            controller,
            monkeypatch,
            capsys,
            commercial_user,
            client_information,
            contract_information,
            support_user,
            event_information):
        self.add_user(controller, commercial_user)
        self.add_user(controller, support_user)
        self.connect_user(controller, 1)
        self.add_client(controller, client_information)
        self.add_contract(controller, contract_information, 1)
        controller.session.status = 'ADD_EVENT'
        inputs = iter(
            [
                '0',
                '0',
                event_information['location'],
                event_information['attendees'],
                event_information['date_start'].strftime('%d/%m/%Y'),
                event_information['date_stop'].strftime('%d/%m/%Y'),
                event_information['notes'],
                event_information['support_contact_id'],
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.add_event()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Ajout d\'un évènement' in captured.out
        assert 'Evènement ajouté' in captured.out

    def test_update_event(
            self,
            controller,
            monkeypatch,
            capsys,
            commercial_user,
            client_information,
            contract_information,
            support_user,
            event_information):
        self.add_user(controller, commercial_user)
        self.add_user(controller, support_user)
        self.connect_user(controller, 1)
        self.add_client(controller, client_information)
        self.add_contract(controller, contract_information, 1)
        self.connect_user(controller, 2)
        self.add_event(controller, event_information, 1, 2)
        controller.session.status = 'UPDATE_EVENT'
        inputs = iter(
            [
                '0',
                '0',
                'la-bas',
                '',
                '',
                '',
                '',
                '',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.update_event()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'la-bas' in captured.out
        assert 'Evènement mis à jour' in captured.out

    def test_update_support_on_event_by_management(
            self,
            controller,
            monkeypatch,
            capsys,
            management_user,
            client_information,
            contract_information,
            support_user,
            event_information):
        self.add_user(controller, management_user)
        self.add_user(controller, support_user)
        self.connect_user(controller, 1)
        self.add_client(controller, client_information)
        self.add_contract(controller, contract_information, 1)
        self.connect_user(controller, 2)
        self.add_event(controller, event_information, 1, 2)
        self.connect_user(controller, 1)
        controller.session.status = 'UPDATE_SUPPORT_ON_EVENT'
        inputs = iter(
            [
                '0',
                '0',
                '',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.update_event()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Evènement mis à jour' in captured.out

    def test_delete_event(
            self,
            controller,
            monkeypatch,
            capsys,
            commercial_user,
            client_information,
            contract_information,
            support_user,
            event_information):
        self.add_user(controller, commercial_user)
        self.add_user(controller, support_user)
        self.connect_user(controller, 1)
        self.add_client(controller, client_information)
        self.add_contract(controller, contract_information, 1)
        self.connect_user(controller, 2)
        self.add_event(controller, event_information, 1, 2)
        controller.session.status = 'DELETE_EVENT'
        inputs = iter(
            [
                '0',
                '0',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        monkeypatch.setattr('rich.prompt.Confirm.ask', lambda *args, **kwargs: True)
        controller.delete_event()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Evènement supprimé' in captured.out

    def test_view_event(
            self,
            controller,
            monkeypatch,
            capsys,
            commercial_user,
            client_information,
            contract_information,
            support_user,
            event_information):
        self.add_user(controller, commercial_user)
        self.add_user(controller, support_user)
        self.connect_user(controller, 1)
        self.add_client(controller, client_information)
        self.add_contract(controller, contract_information, 1)
        self.connect_user(controller, 2)
        self.add_event(controller, event_information, 1, 2)
        controller.session.status = 'VIEW_EVENT'
        inputs = iter(
            [
                '0',
                '0',
                ''
            ]
        )
        monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(inputs))
        controller.view_event()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Informations sur l\'évènement' in captured.out
