class Controller:
    def __init__(self, prompt, show, db):
        self.prompt = prompt()
        self.show = show()
        self.db = db()
        self._user_logged = False
        self.user_id = None

    def first_launch(self):
        if not self.db.has_epic_users():
            self.show.first_launch()
            self.create_user(department_id=3)
        return None

    def user_is_logged(self):
        self.show.login_message()
        if not self._user_logged:
            email = self.prompt.for_email()
            password = self.prompt.for_password()
            if self.db.check_user_login(email, password):
                self.show.logged_ok()
                self._user_logged = True
            else:
                self.show.logged_nok()
        return self._user_logged

    def create_user(self, department_id=None):
        name = self.prompt.for_name()
        email = self.prompt.for_email()
        password = self.prompt.for_password()
        employee_number = self.prompt.for_employee_number()
        if department_id is None:
            department_id = self.prompt.for_department(self.db.get_department_list())
        else:
            department_id = 3
        if self.db.add_user(name, email, password, employee_number, department_id):
            # Show a message
            return True
        # Show a message if not
        return False
