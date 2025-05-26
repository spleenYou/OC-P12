from getpass import getpass


class Prompt:
    def __init__(self):
        pass

    def ask_user_loggin_information(self):
        login = input('Entrez votre login ? ')
        password = getpass('Entrez votre mot de passe : ')
        return login, password
