import os
from functools import wraps


class Show:
    def __init__(self, db, session):
        self.FRAME_LENGHT = 120
        self.SPACE_REQUIRED = 5
        self.NUMBER_SIDE_STARS = 1
        self.STARS_LINE_FULL = "*" * self.FRAME_LENGHT
        self.STARS_LINE = (
            "*" * self.NUMBER_SIDE_STARS
            + " " * (self.FRAME_LENGHT - 2 * self.NUMBER_SIDE_STARS)
            + "*" * self.NUMBER_SIDE_STARS
        )
        self.TOP_DECORATION = "TOP"
        self.BOTTOM_DECORATION = "BOTTOM"
        self.session = session
        self.db = db

    def decoration(function):
        "Contour decoration"

        @wraps(function)
        def text_decorated(self, *args, **kwargs):
            print(self.STARS_LINE_FULL)
            print(self.STARS_LINE)
            function(self, *args, **kwargs)
            print(self.STARS_LINE)
            print(self.STARS_LINE_FULL)
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

        content = [
            (":::::::::: :::::::::  :::::::::::  ::::::::        :::::::::: :::     ::: ::::::::::"
             " ::::    ::: :::::::::::"),
            (":+:        :+:    :+:     :+:     :+:    :+:       :+:        :+:     :+: :+:       "
             " :+:+:   :+:     :+:    "),
            ("+:+        +:+    +:+     +:+     +:+              +:+        +:+     +:+ +:+       "
             " :+:+:+  +:+     +:+    "),
            ("+#++:++#   +#++:++#+      +#+     +#+              +#++:++#   +#+     +:+ +#++:++#  "
             " +#+ +:+ +#+     +#+    "),
            ("+#+        +#+            +#+     +#+              +#+         +#+   +#+  +#+       "
             " +#+  +#+#+#     +#+    "),
            ("#+#        #+#            #+#     #+#    #+#       #+#          #+#+#+#   #+#       "
             " #+#   #+#+#     #+#    "),
            ("########## ###        ###########  ########        ##########     ###     ##########"
             " ###    ####     ###    ")
        ]
        self.show_content(content, 'center')

    @decoration
    def show_content(self, content, align):
        """Shows the content decorated

        Args:
            content (list): list of the content (str) to show
            align (str): Position of contents. Three possiblities left, center or right
        """
        if content:
            for text in content:
                self.decorated_text(text, align)

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
        spaces_needed = self.FRAME_LENGHT - 2 * self.NUMBER_SIDE_STARS - len(text)
        match align:
            case "left":
                spaces_left = self.SPACE_REQUIRED
                spaces_right = spaces_needed - spaces_left
            case "center":
                spaces_left = int(spaces_needed / 2)
                spaces_right = int(spaces_needed / 2)
                if spaces_needed % 2 == 1:
                    spaces_right = spaces_right + 1
        print(
            f"{'*' * self.NUMBER_SIDE_STARS}"
            f"{' ' * spaces_left}{text}"
            f"{' ' * spaces_right}"
            f"{'*' * self.NUMBER_SIDE_STARS}"
        )

    def wait(self):
        "SHow a waiting line if a pause is needed"
        self.display()
        input("Appuyer sur une touche pour continuer...")

    def session_information(self):
        if self.session.user['id'] is not None:
            content = []
            department_name = self.db.get_department_list()[self.session.user['department_id'] - 1]
            content.append(f"Utilisateur : {self.session.user['name']} |"
                           f" Departement : {department_name}")
            self.show_content(content, 'left')

    def title(self):
        title = None
        match self.session.status:
            case 'FIRST_LAUNCH':
                title = 'Premier lancement de l\'application'
            case 'FORBIDDEN':
                title = 'Action interdite'
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
            case 'SELECT_CONTRACT':
                title = 'Selection d\'un contrat'
            case 'NO_CONTRACT':
                title = 'Aucun contract enregistré'
            case 'ADD_EVENT':
                title = 'Ajout d\'un évènement'
            case 'UPDATE_EVENT':
                title = 'Mise à jour d\'un évènement'
            case 'DELETE_EVENT':
                title = 'Suppression d\'un évènement'
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
            case 'HELP':
                title = 'Aide'
            case 'EXIT':
                title = 'Au revoir'
            case _:
                title = None
        if title:
            self.show_content([title], 'center')

    def content(self):
        content = []
        align = 'center'
        match self.session.status:
            case 'FIRST_LAUNCH':
                content.append('Un utilisateur de l\'équipe Management va être créé')
                content.append('afin de pouvoir continuer')
            case 'SELECT_USER':
                users = self.db.get_user_list()
                for index, user in enumerate(users):
                    content.append(f'{index} - ({user.employee_number}) {user.name} \\ {user.email} \\ '
                                   f'{user.department_name}')
            case 'SELECT_CLIENT':
                clients = self.db.get_client_list()
                for index, client in enumerate(clients):
                    content.append(f'{index} - {client.company_name} \\ {client.name}')
            case 'SELECT_CONTRACT':
                contracts = self.db.get_contract_list()
                for index, contract in enumerate(contracts):
                    content.append(f'{index} - {contract.date_creation.strftime("%d %b %Y")} \\ '
                                   f"{contract.total_amount} \\ "
                                   f"{'Terminé' if self.session.contract['status'] else 'En cours'}")
            case 'LOGIN_FAILED':
                content.append('Vos identifiants sont inconnus')
                content.append('L\'application va s\'arrêter')
            case 'ADD_USER_FAILED':
                content.append('Utilisateur non enregistré')
                if self.db.number_of_user() == 0:
                    content.append('')
                    content.append('Il faut au moins un utilisateur pour utiliser l\'application')
                    content.append('')
                    content.append('Fermeture de l\'application')
            case 'MAIN_MENU':
                content.append('Merci d\'entrer la commande correspondant à ce que vous souhaiter faire')
                content.append('Entrer "HELP" pour avoir la description des commandes')
                content.append('Entrer "EXIT" pour quitter l\'application')
            case 'HELP':
                content.append('Liste des actions possibles :')
                content.append('ADD | UPDATE | VIEW | DELETE')
                content.append('')
                content.append('Liste des catégories possibles :')
                content.append('USER | CLIENT | CONTRACT | EVENT')
                content.append('')
                content.append('Syntaxe : ACTION CATEGORIE')
                content.append('')
                content.append(
                    'L\'accès à certaines actions est restreint en fonction des permissions attribuées à '
                    'votre département.'
                )
                content.append('Pour les connaître, taper PERMISSION')
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

        if self.session.status[:3] in ['ADD', 'UPD', 'VIE', 'DEL']:
            if self.session.status[-4:] == 'USER':
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
            if self.session.status[-6:] == 'CLIENT':
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
            if self.session.status[-8:] == 'CONTRACT':
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
        if content:
            self.show_content(content, align)
