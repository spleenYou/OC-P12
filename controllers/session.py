from views.prompt import Prompt
from database.mysql import Mysql


class Session:
    def __init__(self):
        self.prompt = Prompt()
        self.is_logged = False
        self.mysql = Mysql()

    def log_user(self):
        login, password = self.prompt.ask_user_loggin_information()
        return self.mysql.user_exists(login, password)
