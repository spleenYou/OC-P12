class Controller:
    def __init__(self, prompt, show, db, auth, permission, login):
        self.prompt = prompt()
        self.show = show()
        self.db = db()
        self.auth = auth()
        self.permissions = permission(self.db)
        self.permission_level = None
        self.login = login

    def start(self):
        self.show.start()
        if not self.login:
            self.login = self.prompt.for_email()
        if self.db.has_epic_users() == 0:
            self.show.first_launch()
            self.auth.generate_secret_key()
            self.create_user(department_id=3)
        password = self.prompt.for_password()
        self.permission_level = self.db.check_user_login(self.login, password)
        if self.permission_level is not None:
            self.auth.generate_token(self.permission_level)
            self.show.logged_ok()
        else:
            self.show.logged_nok()

    def create_user(self, ask_email=None, department_id=None):
        name = self.prompt.for_name()
        email = self.login
        if ask_email:
            email = self.prompt.for_email()
        password = self.prompt.for_password()
        employee_number = self.prompt.for_employee_number()
        if department_id is None:
            department_id = self.prompt.for_department(self.db.get_department_list())
        else:
            department_id = department_id
        if self.db.add_user(name, email, password, employee_number, department_id):
            # Show a message
            return True
        else:
            # Show a message if not
            return False
