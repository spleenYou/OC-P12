import os
import math
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from functools import wraps


class Show:
    def __init__(self, db, session):
        self.FRAME_LENGHT = 118
        self.SPACE_REQUIRED = 5
        self.NUMBER_SIDE = 1
        self.STARS_LINE_FULL_TOP = '┌' + "─" * self.FRAME_LENGHT + '┐'
        self.STARS_LINE_FULL_BOTTOM = '└' + "─" * self.FRAME_LENGHT + '┘'
        self.STARS_LINE = (
            "│" * self.NUMBER_SIDE
            + " " * (self.FRAME_LENGHT * self.NUMBER_SIDE)
            + "│" * self.NUMBER_SIDE
        )
        self.TOP_DECORATION = "TOP"
        self.BOTTOM_DECORATION = "BOTTOM"
        self.session = session
        self.db = db
        self.rich_console = Console(highlight=False)
        self.common_width = 120

    def decoration(function):
        "Contour decoration"

        @wraps(function)
        def text_decorated(self, *args, **kwargs):
            print(self.STARS_LINE_FULL_TOP)
            print(self.STARS_LINE)
            function(self, *args, **kwargs)
            print(self.STARS_LINE)
            print(self.STARS_LINE_FULL_BOTTOM)
            print()
        return text_decorated

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
        panel = Panel(Align(content, align='center'), width=self.common_width, padding=1)
        self.rich_console.print(panel)

    # @decoration
    def show_content(self, content, align):
        """Shows the content decorated

        Args:
            content (list): list of the content (str) to show
            align (str): Position of contents. Three possiblities left, center or right
        """
        # if content:
        #     for text in content:
        #         self.decorated_text(text, align)
        panel = Panel(Align(content, align=align), width=self.common_width, padding=1)
        self.rich_console.print(panel)

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

    def decorated_text(self, text, align="center"):
        """Shows the text decorated

        Args:
            text (str): Text to show and decorate
            align (str): Position of contents. Three possiblities left, center or right. Default : center
        """
        spaces_needed = self.FRAME_LENGHT * self.NUMBER_SIDE - len(text)
        match align:
            case "left":
                spaces_left = self.SPACE_REQUIRED
                spaces_right = spaces_needed - spaces_left
            case "center":
                spaces_left = int(spaces_needed / 2)
                spaces_right = int(spaces_needed / 2)
                if spaces_needed % 2 == 1:
                    spaces_right = spaces_right + 1
        # print(
        #     f"{'│' * self.NUMBER_SIDE}"
        #     f"{' ' * spaces_left}"
        #     f"{text}"
        #     f"{' ' * spaces_right}"
        #     f"{'│' * self.NUMBER_SIDE}"
        # )
        self.rich_console.print(
            f"{'│' * self.NUMBER_SIDE}"
            f"{' ' * spaces_left}"
            f"{text}"
            f"{' ' * spaces_right}"
            f"{'│' * self.NUMBER_SIDE}"
        )

    def wait(self):
        "SHow a waiting line if a pause is needed"
        self.display()
        input("Appuyer sur une touche pour continuer...")

    def session_information(self):
        if self.session.user['id'] is not None:
            content = []
            department_name = self.db.get_department_list()[self.session.user['department_id'] - 1]
            content = (f"Utilisateur : {self.session.user['name']}\n"
                       f"Departement : {department_name}")
            self.show_content(content, 'left')

    def title(self):
        title = None
        match self.session.status:
            case 'FIRST_LAUNCH':
                title = 'Premier lancement de l\'application'
            case 'FORBIDDEN':
                title = '[bold red]Action interdite[/bold red]'
            case 'ADD_USER':
                title = 'Ajout d\'un utilisateur'
            case 'ADD_USER_OK':
                title = 'Utilisateur créé'
            case 'UPDATE_USER':
                title = 'Mise à jour d\'un utilisateur'
            case 'UPDATE_USER_OK':
                title = 'Utilisateur modifié'
            case 'UPDATE_USER_FAILED':
                title = 'Utilisateur non modifié'
            case 'VIEW_USER':
                title = 'Informations sur un utilisateur'
            case 'DELETE_USER':
                title = 'Suppression d\'un utilisateur'
            case 'DELETE_USER_OK':
                title = 'Utilisateur supprimé'
            case 'SELECT_USER':
                title = 'Sélection d\'un utilisateur'
            case 'SELECT_SUPPORT_USER':
                title = 'Selection d\'un utilisateur support'
            case 'ADD_CLIENT':
                title = 'Ajout d\'un client'
            case 'ADD_CLIENT_OK':
                title = 'Client ajoutè'
            case 'ADD_CLIENT_FAILED':
                title = 'Impossible d\'ajouter le client'
            case 'UPDATE_CLIENT':
                title = 'Mise à jour d\'un client'
            case 'UPDATE_CLIENT_OK':
                title = 'Client mis à jour'
            case 'UPDATE_CLIENT_FAILED':
                title = 'Client non mis à jour'
            case 'DELETE_CLIENT':
                title = 'Suppression d\'un client'
            case 'DELETE_CLIENT_OK':
                title = 'Client supprimé'
            case 'SELECT_CLIENT':
                title = 'Selection d\'un client'
            case 'NO_CLIENT':
                title = 'Aucun client n\'est enregistré'
            case 'ADD_CONTRACT':
                title = 'Ajout d\'un contrat'
            case 'ADD_CONTRACT_OK':
                title = 'Contrat ajouté'
            case 'ADD_CONTRACT_FAILED':
                title = '*impossible d\'ajouter le contrat'
            case 'UPDATE_CONTRACT':
                title = 'Mise à jour d\'un contrat'
            case 'UPDATE_CONTRACT_OK':
                title = 'Contrat mis à jour'
            case 'DELETE_CONTRACT':
                title = 'Suppression d\'un contrat'
            case 'DELETE_CONTRACT_OK':
                title = 'Contrat supprimé'
            case 'DELETE_CONTRACT_FAILED':
                title = 'Contrat non supprimé'
            case 'SELECT_CONTRACT':
                title = 'Selection d\'un contrat'
            case 'NO_CONTRACT':
                title = 'Aucun contract enregistré'
            case 'ADD_EVENT':
                title = 'Ajout d\'un évènement'
            case 'ADD_EVENT_OK':
                title = 'Evènement ajouté'
            case 'ADD_EVENT_FAILED':
                title = 'Evènement non ajouté'
            case 'UPDATE_EVENT' | 'UPDATE_SUPPORT_ON_EVENT':
                title = 'Mise à jour d\'un évènement'
            case 'UPDATE_EVENT_OK':
                title = 'Evènement mis à jour'
            case 'UPDATE_EVENT_failed':
                title = 'Evènement non mis à jour'
            case 'DELETE_EVENT':
                title = 'Suppression d\'un évènement'
            case 'DELETE_EVENT_OK':
                title = 'Evènement supprimé'
            case 'DELETE_EVENT_FAILED':
                title = 'Evènement non supprimé'
            case 'UPDATE_SUPPORT_ON_EVENT':
                title = 'Mise à jour du support'
            case 'CONNECTION':
                title = 'Connexion'
            case 'ERROR' | 'ADD_USER_FAILED' | 'ADD_CLIENT_FAILED':
                title = 'Erreur'
            case 'LOGIN_FAILED':
                title = 'Erreur de connexion'
            case 'LOGIN_OK':
                title = 'Connexion réussie'
            case ('UNKNOWN' |
                  'BAD_EMAIL' |
                  'BAD_EMPLOYEE_NUMBER' |
                  'BAD_EMPLOYEE_NUMBER' |
                  'SELECT_USER_FAILED' |
                  'BAD_SELECT_USE' |
                  'BAD_PHONE' |
                  'SELECT_CLIENT_FAILED' |
                  'BAD_TOTAL_AMOUNT' |
                  'BAD_REST_AMOUNT' |
                  'SELECT_CONTRACT_FAILED' |
                  'BAD_SELECT_CLIENT' |
                  'BAD_CONTRACT_STATUS'):
                title = 'Erreur de saisie'
            case 'PERMISSION':
                title = 'Tableau des permissions'
            case 'HELP':
                title = 'Aide'
            case 'EXIT':
                title = 'Au revoir'
            case _:
                title = None
        if title:
            self.show_content(title, 'center')

    def content(self):
        content = None
        align = 'center'
        match self.session.status:
            case 'FIRST_LAUNCH':
                content = ('Un utilisateur de l\'équipe Management va être créé\n'
                           'afin de pouvoir continuer')
            case 'NO_SUPPORT_USER':
                content = ('Pas d\'utilisateur support enregistré\n\n'
                           'Un utilisateur support est obligatoire pour créer un event')
            case 'SELECT_USER':
                users = self.db.get_user_list()
                lines = [
                    f'{index} - ({user.employee_number}) {user.name} \\ {user.email} \\ '
                    f'{user.department_name}'
                    for index, user in enumerate(users)
                ]
                content = "\n".join(lines)
            case 'SELECT_CLIENT':
                clients = self.db.get_client_list()
                lines = [
                    f'{index} - {client.company_name} \\ {client.name}'
                    for index, client in enumerate(clients)
                ]
                content = "\n".join(lines)
            case 'SELECT_CONTRACT' | 'SELECT_CONTRACT_EVENT':
                with_event = False
                if self.session.status == 'SELECT_CONTRACT_EVENT':
                    with_event = True
                contracts = self.db.get_contract_list(with_event)
                lines = [
                    f'{index} - {contract.date_creation.strftime("%d %b %Y")} \\ '
                    f'{contract.total_amount} \\ '
                    f'{"Terminé" if self.session.contract["status"] else "En cours"}'
                    for index, contract in enumerate(contracts)
                ]
                content = "\n".join(lines)
            case 'SELECT_SUPPORT_USER':
                support_users = self.db.get_support_user_list()
                lines = [
                    f'{index} - {user.name} / {user.email}'
                    for index, user in enumerate(support_users)
                ]
                content = "\n".join(lines)
            case 'LOGIN_FAILED':
                content = ('Vos identifiants sont inconnus'
                           'L\'application va s\'arrêter')
            case 'ADD_USER_FAILED':
                content = 'Utilisateur non enregistré'
                if self.db.number_of_user() == 0:
                    content = content + ('\nIl faut au moins un utilisateur pour utiliser l\'application\n'
                                         'Fermeture de l\'application')
            case 'MAIN_MENU':
                content = ('Merci d\'entrer la commande correspondant à ce que vous souhaiter faire\n'
                           'Entrer "HELP" pour avoir la description des commandes\n'
                           'Entrer "EXIT" pour quitter l\'application')
            case 'HELP':
                content = (
                    """Liste des actions possibles :
ADD | UPDATE | VIEW | DELETE

Liste des catégories possibles :
USER | CLIENT | CONTRACT | EVENT

Syntaxe : ACTION CATEGORIE

L\'accès à certaines actions est restreint en fonction des permissions attribuées à votre département.

Pour les connaître, taper PERMISSION""")
            case 'PERMISSION':
                permissions_table = [
                    'add_user', 'update_user', 'delete_user',
                    'add_client', 'update_client', 'delete_client',
                    'add_contract', 'update_contract', 'delete_contract',
                    'add_event', 'update_event', 'delete_event',
                ]
                content.append('┌' + '─' * 17 + '┬' + '─' * 12 + '┬' + '─' * 9 + '┬' + '─' * 12 + '┐')
                permissions = self.db.get_permissions()
                department_name = self.db.get_department_list()
                head_table = "│     Command     │"
                for perm in permissions:
                    head_table = head_table + f" {department_name[int(perm.department_id) - 1]} │"
                content.append(head_table)
                for perm in permissions_table:
                    commercial_perm = ' ' * 10
                    support_perm = ' '*7
                    management_perm = ' '*10
                    if eval('permissions[0].' + perm):
                        commercial_perm = '    X     '
                    if eval('permissions[1].' + perm):
                        support_perm = '   X   '
                    if eval('permissions[2].' + perm):
                        management_perm = '    X     '
                    if perm == 'update_event':
                        management_perm = '    *     '
                    perm = perm.replace('_', ' ')
                    content.append('├' + '─' * 17 + '┼' + '─' * 12 + '┼' + '─' * 9 + '┼' + '─' * 12 + '┤')
                    content.append(
                        f"│{' ' * (8 - math.floor(len(perm)/2))}{perm}{' ' * (9 - math.ceil(len(perm)/2))}│ "
                        f"{commercial_perm} │ {support_perm} │ {management_perm} │"
                    )
                content.append('└' + '─' * 17 + '┴' + '─' * 12 + '┴' + '─' * 9 + '┴' + '─' * 12 + '┘')
                content.append('')
                content.append('* : Le management peut mettre à jour le contact support d\'un évènement')
            case 'BAD_EMAIL':
                content.append('Votre saisie ne correspond pas à un email.')
            case 'BAD_EMPLOYEE_NUMBER':
                content.append('Votre saisie ne correspond pas à un numéro d\'employé.')
            case 'BAD_DEPARTMENT':
                content.append('Votre saisie ne correspond pas à aucun département.')
            case 'SELECT_USER_FAILED':
                content.append('Ce numéro ne correspond pas à un utilisateur.')
            case ('BAD_SELECT_USER' |
                  'BAD_SELECT_CLIENT' |
                  'BAD_TOTAL_AMOUNT' |
                  'BAD_REST_AMOUNT' |
                  'BAD_SELECT_CONTRACT'):
                content.append('Merci d\'entrer un nombre')
            case 'SELECT_CLIENT_FAILED':
                content.append('Ce numéro ne correspond pas à un client.')
            case 'SELECT_CONTRACT_FAILED':
                content.append('Ce numéro ne correspond pas à un contrat.')
            case 'BAD_PHONE':
                content.append('Numéro de téléphone incorrect')
            case 'UNKNOWN':
                content.append('Cette commande est inconnue, veuillez recommencer.')
            case _:
                pass

        status = self.session.status.split('_')
        if status[0] in ['ADD', 'UPDATE', 'VIEW', 'DELETE']:
            if status[-1] == 'USER':
                align = 'left'
                department_name = ''
                if self.session.new_user['department_id'] is not None:
                    department_name = self.db.get_department_list()[self.session.new_user['department_id'] - 1]
                content.append('Informations sur l\'utilisateur :')
                content.append('')
                content.append(f"{' ' * 4}Nom : {self.session.new_user['name'] or ''}")
                content.append(f"{' ' * 4}Email : {self.session.new_user['email'] or ''}")
                content.append(f"{' ' * 4}Mot de passe : {'**********' if self.session.new_user['password'] else ''}")
                content.append(f"{' ' * 4}Numéro d\'employé : {self.session.new_user['employee_number'] or ''}")
                content.append(f"{' ' * 4}Département : {department_name}")
            elif status[-1] == 'CLIENT':
                align = 'left'
                content.append(f"Commercial correspondant : {self.session.new_user['name']} - "
                               f"{self.session.new_user['email']}")
                self.show_content(content, align)
                content.clear()
                content.append('')
                content.append('Informations sur le client :')
                content.append('')
                content.append(f"{' ' * 4}Nom de l\'entreprise : {self.session.client['company_name'] or ''}")
                content.append(f"{' ' * 4}Nom du contact : {self.session.client['name'] or ''}")
                content.append(f"{' ' * 4}Email : {self.session.client['email'] or ''}")
                content.append(f"{' ' * 4}Téléphone : {self.session.client['phone'] or ''}")
            elif status[-1] == 'CONTRACT':
                align = 'left'
                content.append(f"Commercial : {self.session.new_user['name']} - "
                               f"{self.session.new_user['email']}")
                content.append(f"Client : {self.session.client['company_name']} - "
                               f"{self.session.client['name']}")
                self.show_content(content, align)
                content.clear()
                content.append('Informations sur le contrat :')
                content.append('')
                content.append(f"{' ' * 4}Montant total du contrat : {self.session.contract['total_amount'] or '0'}")
                content.append(f"{' ' * 4}Montant restant à payer : {self.session.contract['rest_amount'] or '0'}")
                content.append(f"{' ' * 4}Statut du contrat : "
                               f"{'Terminé' if self.session.contract['status'] else 'En cours'}")
            elif status[-1] == 'EVENT':
                align = 'left'
                content.append(f"Commercial : {self.session.new_user['name']} - "
                               f"{self.session.new_user['email']}")
                content.append(f"Client : {self.session.client['company_name']} - "
                               f"{self.session.client['name']}")
                content.append(f"Contrat : {'Terminé' if self.session.contract['status'] else 'En cours'}")
                content.append(f"          Reste à payer : {self.session.contract['rest_amount']}/"
                               f"{self.session.contract['total_amount']}")
                self.show_content(content, align)
                content.clear()
                support_user = None
                if self.session.event['support_contact_id'] is not None:
                    support_user = self.db.get_user_information(self.session.event['support_contact_id'])
                date_start = self.session.event['date_start']
                if date_start is not None:
                    date_start = date_start.strftime("%d %b %Y")
                date_stop = self.session.event['date_stop']
                if date_stop is not None:
                    date_stop = date_stop.strftime("%d %b %Y")
                content.append('Informations sur l\'évènement :')
                content.append('')
                content.append(f"Lieu : {self.session.event['location'] or ''}")
                content.append(f"Nombre de personnes : {self.session.event['attendees'] or ''} ")
                content.append(f"Date de début : {date_start or ''}")
                content.append(f"Date de fin : {date_stop or ''}")
                content.append(f"Notes : {self.session.event['notes'] or ''}")
                content.append(f"Support : {support_user['name'] if support_user else ''} - "
                               f"{support_user['email'] if support_user else ''}")
        if content:
            self.show_content(Text(content, justify=align), align)
