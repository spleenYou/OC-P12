import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.text import Text


class Show:
    def __init__(self, db, session):
        self.session = session
        self.db = db
        self.rich_console = Console(highlight=False)
        self.common_width = 120
        self.TITLES = {
            'FIRST_LAUNCH': 'Premier lancement de l\'application',
            'FORBIDDEN': '[bold red]Vous n\'êtes pas autorisé à faire cette action[/bold red]',
            'ADD_USER': 'Ajout d\'un utilisateur',
            'ADD_USER_OK': 'Utilisateur créé',
            'UPDATE_USER': 'Mise à jour d\'un utilisateur',
            'UPDATE_USER_OK': 'Utilisateur mis à jour',
            'UPDATE_USER_FAILED': 'Utilisateur non mis à jour',
            'VIEW_USER': 'Informations sur l\'utilisateur',
            'DELETE_USER': 'Suppression d\'un utilisateur',
            'DELETE_USER_OK': 'Utilisateur supprimé',
            'SELECT_USER': 'Sélection d\'un utilisateur',
            'SELECT_USER_FOR_DELETE': 'Sélection d\'un utilisateur',
            'SELECT_SUPPORT_USER': 'Selection d\'un utilisateur support',
            'ADD_CLIENT': 'Ajout d\'un client',
            'ADD_CLIENT_OK': 'Client ajouté',
            'ADD_CLIENT_FAILED': 'Impossible d\'ajouter le client',
            'UPDATE_CLIENT': 'Mise à jour d\'un client',
            'UPDATE_CLIENT_OK': 'Client mis à jour',
            'UPDATE_CLIENT_FAILED': 'Client non mis à jour',
            'DELETE_CLIENT': 'Suppression d\'un client',
            'DELETE_CLIENT_OK': 'Client supprimé',
            'SELECT_CLIENT': 'Selection d\'un client',
            'SELECT_CLIENT_WITH_EVENT': 'Selection d\'un client',
            'SELECT_CLIENT_WITHOUT_EVENT': 'Selection d\'un client',
            'SELECT_CLIENT_WITH_CONTRACT': 'Selection d\'un client',
            'VIEW_CLIENT': 'Informations sur le client',
            'NO_CLIENT': 'Aucun client n\'est enregistré',
            'ADD_CONTRACT': 'Ajout d\'un contrat',
            'ADD_CONTRACT_OK': 'Contrat ajouté',
            'ADD_CONTRACT_FAILED': '*impossible d\'ajouter le contrat',
            'UPDATE_CONTRACT': 'Mise à jour d\'un contrat',
            'UPDATE_CONTRACT_OK': 'Contrat mis à jour',
            'DELETE_CONTRACT': 'Suppression d\'un contrat',
            'DELETE_CONTRACT_OK': 'Contrat supprimé',
            'DELETE_CONTRACT_FAILED': 'Contrat non supprimé',
            'SELECT_CONTRACT': 'Selection d\'un contrat',
            'SELECT_CONTRACT_WITH_EVENT': 'Selection d\'un contrat',
            'SELECT_CONTRACT_WITHOUT_EVENT': 'Selection d\'un contrat',
            'VIEW_CONTRACT': 'Informations sur le contrat',
            'NO_CONTRACT': 'Aucun contrat n\'est enregistré',
            'ADD_EVENT': 'Ajout d\'un évènement',
            'ADD_EVENT_OK': 'Evènement ajouté',
            'ADD_EVENT_FAILED': 'Evènement non ajouté',
            'UPDATE_EVENT': 'Mise à jour de l\'évènement',
            'UPDATE_EVENT_OK': 'Evènement mis à jour',
            'UPDATE_EVENT_failed': 'Evènement non mis à jour',
            'DELETE_EVENT': 'Suppression d\'un évènement',
            'DELETE_EVENT_OK': 'Evènement supprimé',
            'DELETE_EVENT_FAILED': 'Evènement non supprimé',
            'UPDATE_SUPPORT_ON_EVENT': 'Mise à jour du support',
            'VIEW_EVENT': 'Informations sur l\'évènement',
            'NO_EVENT': 'Aucun évènement n\'est enregistré',
            'CONNECTION': 'Connexion',
            'ERROR': 'Erreur',
            'ADD_USER_FAILED': 'Erreur',
            'LOGIN_FAILED': 'Erreur de connexion',
            'LOGIN_OK': '[green]Connexion réussie[/green]',
            'UNKNOWN': 'Erreur de saisie',
            'BAD_SELECT_CONTRACT': 'Erreur de saisie',
            'BAD_EMAIL': 'Erreur de saisie',
            'BAD_EMPLOYEE_NUMBER': 'Erreur de saisie',
            'SELECT_USER_FAILED': 'Erreur de saisie',
            'BAD_SELECT_USE': 'Erreur de saisie',
            'BAD_PHONE': 'Erreur de saisie',
            'SELECT_CLIENT_FAILED': 'Erreur de saisie',
            'BAD_DEPARTMENT': 'Erreur de saisie',
            'BAD_TOTAL_AMOUNT': 'Erreur de saisie',
            'BAD_REST_AMOUNT': 'Erreur de saisie',
            'BAD_DATE_START': 'Erreur de saisie',
            'BAD_DATE_STOP': 'Erreur de saisie',
            'PASSWORD_EMPTY': 'Erreur de saisie',
            'SELECT_CONTRACT_FAILED': 'Erreur de saisie',
            'BAD_SELECT_CLIENT': 'Erreur de saisie',
            'BAD_CONTRACT_STATUS': 'Erreur de saisie',
            'PERMISSION': 'Tableau des permissions',
            'HELP': 'Aide',
            'EXIT': 'Au revoir',
            'MAIN_MENU': 'Menu principal',
            'PASSWORD_FIRST_TIME': 'Définition du mot de passe',
            'PASSWORD_SECOND_TIME': 'Définition du mot de passe',
            'PASSWORD_MATCH_FAILED': 'Erreur de saisie',
            'BAD_TOKEN': 'Déconnexion automatique'
        }
        self.SIMPLE_CONTENTS = {
            'FIRST_LAUNCH': ('Un utilisateur de l\'équipe Management va être créé\n'
                             'afin de pouvoir continuer'),
            'NO_CLIENT_WITHOUT_EVENT': 'Pas de client avec contrat sans évènement',
            'BAD_EMAIL': 'Votre saisie ne correspond pas à une adresse mail.',
            'BAD_EMPLOYEE_NUMBER': 'Votre saisie ne correspond pas à un numéro d\'employé.',
            'BAD_DEPARTMENT': 'Votre saisie ne correspond pas à un département.',
            'SELECT_USER_FAILED': 'Ce numéro ne correspond pas à un utilisateur.',
            'BAD_SELECT_USER': 'Merci d\'entrer un nombre',
            'BAD_SELECT_CLIENT': 'Merci d\'entrer un nombre',
            'BAD_TOTAL_AMOUNT': 'Merci d\'entrer un nombre',
            'BAD_REST_AMOUNT': 'Merci d\'entrer un nombre',
            'BAD_SELECT_CONTRACT': 'Merci d\'entrer un nombre',
            'SELECT_CLIENT_FAILED': 'Ce numéro ne correspond pas à un client.',
            'SELECT_CONTRACT_FAILED': 'Ce numéro ne correspond pas à un contrat.',
            'BAD_PHONE': 'Numéro de téléphone incorrect',
            'UNKNOWN': 'Cette commande est inconnue, veuillez recommencer.',
            'MAIN_MENU': ('Merci d\'entrer la commande correspondant à ce que vous souhaitez faire\n\n'
                          'Entrer "HELP" pour avoir la description des commandes\n'
                          'Entrer "EXIT" pour quitter l\'application'),
            'HELP': ('Liste des actions possibles :\n '
                     'ADD | UPDATE | VIEW | DELETE\n\n '
                     'Liste des catégories possibles :\n '
                     'USER | CLIENT | CONTRACT | EVENT\n\n '
                     'Syntaxe : ACTION CATEGORIE\n\n'
                     'L\'accès à certaines actions est restreint en fonction des permissions'
                     ' attribuées à votre département.\n\n'
                     'Pour les connaître, taper PERMISSION'),
            'LOGIN_FAILED': ('Vos identifiants sont inconnus\n'
                             'L\'application va s\'arrêter'),
            'PASSWORD_FIRST_TIME': 'Bienvenue pour votre première connexion.\n\nVeuillez définir votre mot de passe',
            'PASSWORD_SECOND_TIME': ('Bienvenue pour votre première connexion.\n\n'
                                     'Veuillez entrer une deuxième fois votre mot de passe'),
            'PASSWORD_MATCH_FAILED': 'Les mots de passe ne sont pas identiques',
            'BAD_CONTRACT_STATUS': 'Cette réponse n\'est pas possible.\n\nMerci d\'indiquer y or n comme demandé',
            'PASSWORD_EMPTY': 'Votre mot de passe ne peut pas être vide.',
            'BAD_TOKEN': 'Vous avez été déconnecté, merci de vous reconnecter.'
        }

    def display(self, content=None, align='center'):
        """Manages the display on the console

        Args:
            title (str): Title to show
            content (list): List of the text to show
            align (str): Position of the content. Three possiblities left, center or right
        """
        self.clear_screen()
        self.head_menu()
        self.session_information()
        self.title()
        self.content()

    def show_content(self, content, align, border_style):
        """Shows the content decorated

        Args:
            content (list): list of the content (str) to show
            align (str): Position of contents. Three possiblities left, center or right
        """
        panel = Panel(
            Align(content, align=align, style='dark_orange3'),
            width=self.common_width,
            padding=1,
            border_style=border_style
        )
        self.rich_console.print(panel)

    def clear_screen(self):
        "Clean the console for all os"

        command = "clear"
        if os.name in ("nt", "dos"):
            command = "cls"
        os.system(command)

    def head_menu(self):
        "Shows the name of the program decorated"

        content = (":::::::::: :::::::::  :::::::::::  ::::::::        :::::::::: :::     ::: ::::::::::"
                   " ::::    ::: :::::::::::\n"
                   ":+:        :+:    :+:     :+:     :+:    :+:       :+:        :+:     :+: :+:       "
                   " :+:+:   :+:     :+:    \n"
                   "+:+        +:+    +:+     +:+     +:+              +:+        +:+     +:+ +:+       "
                   " :+:+:+  +:+     +:+    \n"
                   "+#++:++#   +#++:++#+      +#+     +#+              +#++:++#   +#+     +:+ +#++:++#  "
                   " +#+ +:+ +#+     +#+    \n"
                   "+#+        +#+            +#+     +#+              +#+         +#+   +#+  +#+       "
                   " +#+  +#+#+#     +#+    \n"
                   "#+#        #+#            #+#     #+#    #+#       #+#          #+#+#+#   #+#       "
                   " #+#   #+#+#     #+#    \n"
                   "########## ###        ###########  ########        ##########     ###     ##########"
                   " ###    ####     ###    ")
        self.show_content(content, 'center', 'cyan')

    def session_information(self):
        if self.session.user.id is not None and self.session.status != 'LOGIN_OK':
            content = []
            content = (f"    Utilisateur : {self.session.user.name}\n"
                       f"    Departement : {self.session.user.department_name}")
            self.show_content(content, 'left', 'cyan')

    def title(self):
        border_style = 'cyan'
        status = self.session.status.split('_')
        if status[0] in ['BAD', 'UNKNOWN'] or status[-1] == 'FAILED':
            border_style = 'red'
        elif status[-1] == 'OK':
            border_style = 'green'
        text_color = 'dark_orange3' if border_style == 'cyan' else border_style
        self.show_content(
            f'[bold {text_color}]' + self.TITLES[self.session.status] + f'[/bold {text_color}]',
            'center',
            border_style
        )

    def content(self):
        content = None
        align = 'center'
        if self.session.status in self.SIMPLE_CONTENTS:
            self.show_content(Text(self.SIMPLE_CONTENTS[self.session.status], justify=align), align, 'cyan')
            return None
        match self.session.status:
            case 'SELECT_USER' | 'SELECT_USER_FOR_DELETE':
                users = self.db.get_user_list()
                content = Table(show_lines=True)
                content.add_column('N°', justify='left')
                content.add_column('Numéro employé', justify='left')
                content.add_column('Nom', justify='left')
                content.add_column('Email', justify='left')
                content.add_column('Département', justify='left')
                for index, user in enumerate(users):
                    content.add_row(
                        str(index),
                        str(user.employee_number),
                        user.name,
                        user.email,
                        user.department_name
                    )
                self.show_content(content, align, 'cyan')
                content = ''
            case ('SELECT_CLIENT' |
                  'SELECT_CLIENT_WITH_EVENT' |
                  'SELECT_CLIENT_WITHOUT_EVENT' |
                  'SELECT_CLIENT_WITH_CONTRACT'):
                clients = self.db.get_client_list()
                lines = [
                    f'{index} - {client.company_name} \\ {client.name}'
                    for index, client in enumerate(clients)
                ]
                content = "\n".join(lines)
            case 'SELECT_CONTRACT' | 'SELECT_CONTRACT_WITH_EVENT' | 'SELECT_CONTRACT_WITHOUT_EVENT':
                if self.session.status == 'SELECT_CONTRACT':
                    contracts = self.session.client.contracts
                else:
                    contracts = self.db.get_contract_list()
                lines = [
                    f'{index} - {contract.date_creation.strftime("%d %b %Y")} \\ '
                    f'{contract.total_amount} \\ '
                    f'{"Terminé" if contract.status else "En cours"}'
                    for index, contract in enumerate(contracts)
                ]
                content = "\n".join(lines)
            case 'SELECT_SUPPORT_USER':
                support_users = self.db.get_support_user_list()
                content = Table(show_header=False)
                content.add_column(justify='left')
                content.add_column(justify='left')
                content.add_column(justify='left')
                for index, user in enumerate(support_users):
                    content.add_row(str(index), user.name, user.email)
            case 'ADD_USER_FAILED':
                content = 'Utilisateur non enregistré'
                if self.db.number_of_user() == 0:
                    content = content + ('\nIl faut au moins un utilisateur pour utiliser l\'application\n'
                                         'Fermeture de l\'application')
            case 'PERMISSION':
                permissions_table = [
                    'add_user', 'update_user', 'delete_user',
                    'add_client', 'update_client', 'delete_client',
                    'add_contract', 'update_contract', 'delete_contract',
                    'add_event', 'update_event', 'delete_event',
                ]
                permissions = self.db.get_permissions()
                department_name = self.db.get_department_list()
                content = Table(show_lines=True)
                content.add_column("    Command", justify='left')
                for perm in permissions:
                    content.add_column(department_name[int(perm.department_id) - 1], justify='center')
                for perm in permissions_table:
                    commercial_perm = ''
                    support_perm = ''
                    management_perm = ''
                    if eval('permissions[0].' + perm):
                        commercial_perm = 'X'
                    if eval('permissions[1].' + perm):
                        support_perm = 'X'
                    if eval('permissions[2].' + perm):
                        management_perm = 'X'
                    if perm == 'update_event':
                        management_perm = '*'
                    perm = perm.replace('_', ' ')
                    content.add_row(perm, commercial_perm, support_perm, management_perm)
                content = '* : Le management peut mettre à jour le contact support d\'un évènement'

        status = self.session.status.split('_')
        if (status[0] in ['ADD', 'UPDATE', 'VIEW', 'DELETE'] and
                status[-1] in ['USER', 'CLIENT', 'CONTRACT', 'EVENT']):
            content = Table(show_header=False, show_lines=True)
            content.add_column(justify='left')
            content.add_column(justify='left')
            if status[-1] == 'USER':
                department_name = ''
                if self.session.new_user.department_id is not None:
                    department_name = self.db.get_department_list()[self.session.new_user.department_id - 1]
                employee_number = self.session.new_user.employee_number or ''
                content.add_row('Nom', self.session.new_user.name or '')
                content.add_row('Email', self.session.new_user.email or '')
                content.add_row('Numéro d\'employé', str(employee_number))
                content.add_row('Département', department_name)
            elif status[-1] == 'CLIENT':
                content.add_row('Nom de l\'entreprise', self.session.client.company_name or '')
                content.add_row('Nom du contact', self.session.client.name or '')
                content.add_row('Email', self.session.client.email or '')
                content.add_row('Téléphone', self.session.client.phone or '')
                content.add_row('Commercial', (f"{self.session.client.commercial_contact.name} - "
                                               f"{self.session.client.commercial_contact.email}"))
            elif status[-1] == 'CONTRACT':
                content.add_row('Client', self.session.client.company_name + ' - ' + self.session.client.name)
                content.add_row('Commercial', (f"{self.session.client.commercial_contact.name} - "
                                               f"{self.session.client.commercial_contact.name}"))
                content.add_row('Montant total', str(self.session.contract.total_amount or '0'))
                content.add_row('Reste à payer', str(self.session.contract.rest_amount or '0'))
                content.add_row('Statut', 'Terminé' if self.session.contract.status else 'En cours')
            elif status[-1] == 'EVENT':
                support_user = None
                if self.session.contract.event.support_contact_id is not None:
                    support_user = self.session.contract.event.support_contact
                date_start = self.session.contract.event.date_start
                if date_start is not None:
                    date_start = date_start.strftime("%d %b %Y")
                date_stop = self.session.contract.event.date_stop
                if date_stop is not None:
                    date_stop = date_stop.strftime("%d %b %Y")
                content.add_row('Client', self.session.client.company_name + ' - ' + self.session.client.name)
                content.add_row('Commercial', (f"{self.session.client.commercial_contact.name} - "
                                               f"{self.session.client.commercial_contact.email}"))
                content.add_row('Support',
                                (support_user.name if support_user else '') +
                                ' - ' +
                                support_user.email if support_user else '')
                content.add_row('Statut du contrat', 'Terminé' if self.session.contract.status else 'En cours')
                content.add_row('Reste à payer', f"{self.session.contract.rest_amount}")
                content.add_row('Lieu', self.session.contract.event.location or '')
                content.add_row('Nombre de personnes', str(self.session.contract.event.attendees) or '')
                content.add_row('Date de début', date_start or '')
                content.add_row('Date de fin', date_stop or '')
                content.add_row('Notes', self.session.contract.event.notes or '')
        if content:
            if isinstance(content, str):
                self.show_content(Text(content, justify=align), align, 'cyan')
            else:
                self.show_content(content, align, 'cyan')
