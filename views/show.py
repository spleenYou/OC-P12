import os
import constants as C
from functools import wraps


class Show:
    def __init__(self, session):
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

    def logged_ok(self):
        print('Hello :)')

    def first_launch(self):
        self.display(['Nous allons procéder à la création du premier utilisateur'], 'center')

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
    def title_menu(self):
        "Shows the title decorated"
        self.decorated_text(self.find_title())

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
        self.title_menu()
        content, align = self.find_content()
        if len(content) > 0:
            self.show_content(content, align)

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

    def wait(self):
        "SHow a waiting line if a pause is needed"
        self.display()
        input("Appuyer sur une touche pour continuer...")

    def find_title(self):
        match self.session.status:
            case C.FIRST_LAUNCH:
                return 'Premier lancement de l\'application'
            case C.ADD_USER:
                return 'Ajout d\'un utilisateur'
            case C.FORBIDDEN:
                return 'Action interdite'
            case C.UPDATE_USER:
                return 'Mise à jour d\'un utilisateur'
            case C.DELETE_USER:
                return 'Suppression d\'un utilisateur'
            case C.ADD_CLIENT:
                return 'Ajout d\'un client'
            case C.UPDATE_CLIENT:
                return 'Mise à jour d\'un client'
            case C.DELETE_CLIENT:
                return 'Suppression d\'un client'
            case C.ADD_CONTRACT:
                return 'Ajout d\'un contrat'
            case C.UPDATE_CONTRACT:
                return 'Mise à jour d\'un contrat'
            case C.DELETE_CONTRACT:
                return 'Suppression d\'un contrat'
            case C.ADD_EVENT:
                return 'Ajout d\'un évènement'
            case C.UPDATE_EVENT:
                return 'Mise à jour d\'un évènement'
            case C.DELETE_EVENT:
                return 'Suppression d\'un évènement'
            case C.UPDATE_SUPPORT_ON_EVENT:
                return 'Mise à jour du support'
            case C.CONNECTION:
                return 'Connection'
            case C.ERROR:
                return 'Erreur'
            case C.LOGIN_FAILED:
                return 'Login failed'

    def find_content(self):
        content = []
        align = 'center'
        match self.session.status:
            case C.ADD_USER | C.UPDATE_USER:
                align = 'left'
                content.append('Informations sur l\'utilisateur :')
                content.append('')
                content.append(f"{' ' * 4}Name : {self.session.new_user.name or ''}")
                content.append(f"{' ' * 4}Email : {self.session.new_user.email or ''}")
                content.append(f"{' ' * 4}Password : {'*'*len(self.session.new_user.password or '') or ''}")
                content.append(f"{' ' * 4}Employee number : {self.session.new_user.employee_number or ''}")
                content.append(f"{' ' * 4}Department : {self.session.new_user.department_name or 'Management'}")
            # case C.FORBIDDEN:
            #     return 'Action interdite'
            # case C.UPDATE_USER:
            #     return 'Mise à jour d\'un utilisateur'
            # case C.DELETE_USER:
            #     return 'Suppression d\'un utilisateur'
            # case C.ADD_CLIENT:
            #     return 'Ajout d\'un client'
            # case C.UPDATE_CLIENT:
            #     return 'Mise à jour d\'un client'
            # case C.DELETE_CLIENT:
            #     return 'Suppression d\'un client'
            # case C.ADD_CONTRACT:
            #     return 'Ajout d\'un contrat'
            # case C.UPDATE_CONTRACT:
            #     return 'Mise à jour d\'un contrat'
            # case C.DELETE_CONTRACT:
            #     return 'Suppression d\'un contrat'
            # case C.ADD_EVENT:
            #     return 'Ajout d\'un évènement'
            # case C.UPDATE_EVENT:
            #     return 'Mise à jour d\'un évènement'
            # case C.DELETE_EVENT:
            #     return 'Suppression d\'un évènement'
            # case C.UPDATE_SUPPORT_ON_EVENT:
            #     return 'Ajout d\'un utilisateur'
            # case C.CONNECTION:
            #     return 'Ajout d\'un utilisateur'
            # case C.ERROR:
            #     return None
            case C.LOGIN_FAILED:
                content.append('Vos identifiants sont inconnus')
                content.append('L\'application va s\'arrêter')
            case _:
                pass
        return content, align
