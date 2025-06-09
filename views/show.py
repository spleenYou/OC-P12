import os
import constants as C
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
            ":::::::::: :::::::::  :::::::::::  ::::::::        :::::::::: :::     ::: ::::::::::" +
            " ::::    ::: :::::::::::",
            ":+:        :+:    :+:     :+:     :+:    :+:       :+:        :+:     :+: :+:       " +
            " :+:+:   :+:     :+:    ",
            "+:+        +:+    +:+     +:+     +:+              +:+        +:+     +:+ +:+       " +
            " :+:+:+  +:+     +:+    ",
            "+#++:++#   +#++:++#+      +#+     +#+              +#++:++#   +#+     +:+ +#++:++#  " +
            " +#+ +:+ +#+     +#+    ",
            "+#+        +#+            +#+     +#+              +#+         +#+   +#+  +#+       " +
            " +#+  +#+#+#     +#+    ",
            "#+#        #+#            #+#     #+#    #+#       #+#          #+#+#+#   #+#       " +
            " #+#   #+#+#     #+#    ",
            "########## ###        ###########  ########        ##########     ###     ##########" +
            " ###    ####     ###    "
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
        if text == self.TOP_DECORATION:
            print(self.STARS_LINE_FULL)
            print(self.STARS_LINE)
        elif text == self.BOTTOM_DECORATION:
            print(self.STARS_LINE)
            print(self.STARS_LINE_FULL)
        elif text == self.STARS_LINE_FULL:
            print(self.STARS_LINE_FULL)
        else:
            spaces_needed = self.FRAME_LENGHT - 2 * self.NUMBER_SIDE_STARS - len(text)
            match align:
                case "left":
                    spaces_left = self.SPACE_REQUIRED
                    spaces_right = spaces_needed - spaces_left
                case "right":
                    spaces_right = self.SPACE_REQUIRED
                    spaces_left = spaces_needed - spaces_right
                case "center":
                    spaces_left = int(spaces_needed / 2)
                    spaces_right = int(spaces_needed / 2)
                    if spaces_needed % 2 == 1:
                        spaces_right = spaces_right + 1
                case _:
                    spaces_left = self.SPACE_REQUIRED
                    spaces_right = self.SPACE_REQUIRED
            print(
                f"{'*' * self.NUMBER_SIDE_STARS}"
                f"{' ' * spaces_left}{text}"
                f"{' ' * spaces_right}"
                f"{'*' * self.NUMBER_SIDE_STARS}"
            )

    def add_separator(self, content):
        content.append('')
        content.append(self.STARS_LINE_FULL)
        content.append('')
        return content

    def wait(self):
        "SHow a waiting line if a pause is needed"
        self.display()
        input("Appuyer sur une touche pour continuer...")

    def session_information(self):
        if self.session.user['id'] is not None:
            content = []
            content.append(f"Utilisateur : {self.session.user['name']} | Departement : {self.db.get_department_name()}")
            self.show_content(content, 'left')

    def title(self):
        content = []
        match self.session.status:
            case C.FIRST_LAUNCH:
                content.append('Premier lancement de l\'application')
            case C.ADD_USER:
                content.append('Ajout d\'un utilisateur')
            case C.FORBIDDEN:
                content.append('Action interdite')
            case C.UPDATE_USER:
                content.append('Mise à jour d\'un utilisateur')
            case C.DELETE_USER:
                content.append('Suppression d\'un utilisateur')
            case C.ADD_CLIENT:
                content.append('Ajout d\'un client')
            case C.UPDATE_CLIENT:
                content.append('Mise à jour d\'un client')
            case C.DELETE_CLIENT:
                content.append('Suppression d\'un client')
            case C.ADD_CONTRACT:
                content.append('Ajout d\'un contrat')
            case C.UPDATE_CONTRACT:
                content.append('Mise à jour d\'un contrat')
            case C.DELETE_CONTRACT:
                content.append('Suppression d\'un contrat')
            case C.ADD_EVENT:
                content.append('Ajout d\'un évènement')
            case C.UPDATE_EVENT:
                content.append('Mise à jour d\'un évènement')
            case C.DELETE_EVENT:
                content.append('Suppression d\'un évènement')
            case C.UPDATE_SUPPORT_ON_EVENT:
                content.append('Mise à jour du support')
            case C.CONNECTION:
                content.append('Connexion')
            case C.ERROR | C.ADD_USER_FAILED:
                content.append('Erreur')
            case C.LOGIN_FAILED:
                content.append('Erreur de connexion')
            case C.LOGIN_OK:
                content.append('Connexion réussie')
            case _:
                return None
        if content:
            self.show_content(content, 'center')

    def content(self):
        content = []
        align = 'center'
        match self.session.status:
            case C.FIRST_LAUNCH:
                content.append('Un utilisateur de l\'équipe Management va être créé')
                content.append('afin de pouvoir continuer')
            case C.ADD_USER | C.UPDATE_USER:
                department_name = self.db.get_department_name()
                align = 'left'
                content.append('Informations sur l\'utilisateur :')
                content.append('')
                content.append(f"{' ' * 4}Name : {self.session.new_user['name'] or ''}")
                content.append(f"{' ' * 4}Email : {self.session.new_user['email'] or ''}")
                content.append(f"{' ' * 4}Password : {'*'*len(self.session.new_user['password'] or '') or ''}")
                content.append(f"{' ' * 4}Employee number : {self.session.new_user['employee_number'] or ''}")
                content.append(f"{' ' * 4}Department : {department_name}")
            case C.LOGIN_FAILED:
                content.append('Vos identifiants sont inconnus')
                content.append('L\'application va s\'arrêter')
            case C.ADD_USER_FAILED:
                content.append('Utilisateur non enregistré')
                if not self.db.has_users():
                    content.append('')
                    content.append('Il faut au moins un utilisateur pour utiliser l\'application')
                    content.append('')
                    content.append('Fermeture de l\'application')
            case C.MAIN_MENU:
                content.append('Merci d\'entrer la commande correspondant à ce que vous souhaiter faire')
                content.append('Entrer "HELP" pour avoir la description des commandes')
            case _:
                pass
        if content:
            self.show_content(content, align)
