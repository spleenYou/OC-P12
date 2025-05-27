class Controller:
    def __init__(self, prompt, show, db):
        self.prompt = prompt()
        self.show = show()
        self.db = db()
        self.user_logged = False

    def first_launch(self):
        if not self.db.has_epic_users():
            self.create_user()

    def user_is_logged(self):
        if not self.user_logged:
            login, password = self.prompt.ask_user_loggin_information()
            if self.db.user_exists(login, password):
                self.show.logged_ok()
                self.user_logged = True
            else:
                self.show.logged_nok()
        return self.user_logged

    def create_user(self):
        name = self.prompt.for_name()
        email = self.prompt.for_email()
        password = self.prompt.for_password()
        employee_number = self.prompt.for_employee_number()
        department_id = self.prompt.for_department(self.db.get_department_list())
        if self.db.add_user(name, email, password, employee_number, department_id):
            print('Add ok')
            return True
        print('Add nok')
        return False
