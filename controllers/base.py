class Controller:
    def __init__(self, prompt, show, engine):
        self.prompt = prompt()
        self.show = show()
        self.engine = engine()
        self.user_logged = False

    def first_launch(self):
        if self.engine.has_epic_users():
            return True
        return False

    def user_is_logged(self):
        if not self.user_logged:
            login, password = self.prompt.ask_user_loggin_information()
            if self.engine.user_exists(login, password):
                self.show.logged_ok()
                self.user_logged = True
            else:
                self.show.logged_nok()
        return self.user_logged
