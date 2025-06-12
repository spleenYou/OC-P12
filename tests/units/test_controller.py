from controllers.base import Controller
from controllers.authentication import Authentication
from controllers.db import Mysql
from views.prompt import Prompt
from views.show import Show


class TestController:
    def test_init_controller(session):
        ctrl = Controller(Prompt, Show, Mysql, Authentication, session)
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

    def add_event(self, controller, event):
        controller.session.event = event
        controller.db.add_event()
        controller.session.reset_session()

    def connect_user(self, controller, user_id):
        controller.session.user = controller.db.get_user_information(user_id)
        controller.auth.generate_token()

    def test_start_without_user_and_no_registration(self, monkeypatch, controller, management_user, capsys):
        inputs = iter(
            [
                '',
                management_user['name'],
                management_user['email'],
                management_user['employee_number'],
                'n',
                ''
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('views.prompt.getpass', lambda _: management_user['password'])
        controller.start(None)
        captured = capsys.readouterr()
        assert 'Premier lancement de l\'application' in captured.out
        assert 'Utilisateur non enregistré' in captured.out

    def test_start_without_user_and_with_registration_and_login(self, monkeypatch, controller, management_user, capsys):
        inputs = iter(
            [
                '',
                management_user['name'],
                management_user['email'],
                management_user['employee_number'],
                'y',
                '',
                management_user['email'],
                ''
            ]
        )
        inputs_password = iter(
            [
                management_user['password'],
                management_user['password']
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('views.prompt.getpass', lambda _: next(inputs_password))
        controller.start(None)
        captured = capsys.readouterr()
        assert 'Premier lancement de l\'application' in captured.out
        assert 'Utilisateur créé' in captured.out
        assert 'Connexion' in captured.out
        assert 'Connexion réussie' in captured.out
        expected_text = (f"Utilisateur : {management_user['name']} | "
                         f"Departement : {controller.db.get_department_list()[2]}")
        assert expected_text in captured.out

    def test_start_with_user_and_login_failed(self, monkeypatch, controller, management_user, capsys):
        controller.session.new_user = management_user
        controller.db.add_user()
        controller.session.user = controller.db.get_user_information(1)
        inputs = iter(
            [
                management_user['email'],
                ''
            ]
        )
        inputs_password = iter(
            [
                management_user['password'] + 'e'
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('views.prompt.getpass', lambda _: next(inputs_password))
        controller.start(None)
        captured = capsys.readouterr()
        assert 'Erreur de connexion' in captured.out
        assert 'Vos identifiants sont inconnus' in captured.out

    def test_login_and_try_email_not_correct(self, monkeypatch, controller, management_user, capsys):
        controller.session.new_user = management_user
        controller.db.add_user()
        controller.session.user = controller.db.get_user_information(1)
        inputs = iter(
            [
                'bad_email',
                '',
                management_user['email'],
                ''
            ]
        )
        inputs_password = iter(
            [
                management_user['password'] + 'e'
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('views.prompt.getpass', lambda _: next(inputs_password))
        controller.start(None)
        captured = capsys.readouterr()
        assert 'Erreur de saisie' in captured.out
        assert 'Votre saisie ne correspond pas à un email.' in captured.out

    def test_main_menu(self, controller, monkeypatch, management_user, capsys):
        self.add_user(controller, management_user)
        self.connect_user(controller, 1)
        inputs = iter(
            [
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Merci d\'entrer la commande correspondant à ce que vous souhaiter faire' in captured.out
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
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Erreur de saisie' in captured.out
        assert 'Cette commande est inconnue, veuillez recommencer' in captured.out

    def test_exit_command(self, controller, monkeypatch, management_user, capsys):
        self.add_user(controller, management_user)
        self.connect_user(controller, 1)
        inputs = iter(
            [
                'exit',
                ''
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
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
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        controller.main_menu()
        captured = capsys.readouterr()
        assert 'Aide' in captured.out
        assert 'Liste des actions possibles :' in captured.out
        assert 'ADD | UPDATE | VIEW | DELETE' in captured.out
        assert 'Liste des catégories possibles :' in captured.out
        assert 'USER | CLIENT | CONTRACT | EVENT' in captured.out
        assert 'Syntaxe : ACTION CATEGORIE' in captured.out

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
                'y'
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('views.prompt.getpass', lambda _: commercial_user['password'])
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
                'y'
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('views.prompt.getpass', lambda _: '')
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
                0,
                'y'
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        controller.delete_user()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Utilisateur supprimé' in captured.out

    def test_view_user(self, controller, monkeypatch, management_user, capsys, commercial_user):
        self.add_user(controller, management_user)
        self.connect_user(controller, 1)
        self.add_user(controller, commercial_user)
        controller.session.status = 'VIEW_USER'
        monkeypatch.setattr('builtins.input', lambda _: 1)
        controller.view_user()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Informations sur un utilisateur' in captured.out

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
                'y'
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        controller.add_client()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Client ajoutè' in captured.out

    def test_update_client(self, controller, monkeypatch, capsys, commercial_user, client_information):
        self.add_user(controller, commercial_user)
        self.connect_user(controller, 1)
        self.add_client(controller, client_information)
        controller.session.status = 'UPDATE_CLIENT'
        inputs = iter(
            [
                0,
                'Nouvelle entreprise',
                '',
                '',
                '',
                'y'
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
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
                0,
                'y'
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        controller.delete_client()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Client supprimé' in captured.out

    def test_view_client(self, controller, monkeypatch, capsys, commercial_user, client_information):
        self.add_user(controller, commercial_user)
        self.connect_user(controller, 1)
        self.add_client(controller, client_information)
        controller.session.status = 'VIEW_CLIENT'
        monkeypatch.setattr('builtins.input', lambda _: 0)
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
                0,
                contract_information['total_amount'],
                contract_information['total_amount'],
                'y'
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
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
                0,
                0,
                '',
                0,
                'y',
                'y'
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
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
                0,
                0,
                'y'
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        controller.delete_contract()
        controller.show.display()
        captured = capsys.readouterr()
        for capt in captured:
            print(capt)
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
        inputs = iter([0, 0])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        controller.view_contract()
        controller.show.display()
        captured = capsys.readouterr()
        assert 'Informations sur le contrat' in captured.out
