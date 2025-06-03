class Controller:
    def __init__(self, prompt, show, db, auth):
        self.prompt = prompt()
        self.show = show()
        self.db = db()
        self.auth = auth()
        self.user_info = None

    def start(self, user):
        self.show.start()
        self.user_info = user
        if not self.user_info.email:
            self.user_info.email = self.prompt.for_email()
        if self.db.has_epic_users() == 0:
            self.show.first_launch()
            self.auth.generate_secret_key()
            self.add_user(department_id=3)
        password = self.prompt.for_password()
        self.user_info = self.db.check_user_login(self.user_info.email, password)
        if self.user_info:
            self.auth.generate_token(self.user_info.department_id)
            self.show.logged_ok()
        else:
            self.show.logged_nok()

    def add_user(self, ask_email=None, department_id=None):
        name = self.prompt.for_name()
        if ask_email:
            email = self.prompt.for_email()
        else:
            email = self.user_info.email
        password = self.prompt.for_password()
        employee_number = self.prompt.for_employee_number()
        if department_id is None:
            department_id = self.prompt.for_department(self.db.get_department_list())
        else:
            department_id = department_id
        if self.db.add_epic_user(name, email, password, employee_number, department_id):
            # Show a message
            return True
        else:
            # Show a message if not
            return False

    # def add_client(self):
    #     name = ""
    #     email = ""
    #     phone = ''
    #     entreprise_name = ''
    #     return self.db.add_in_db(
    #         Client(
    #             name=name,
    #             email=email,
    #             phone=phone,
    #             entreprise_name=entreprise_name,
    #             commercial_contact_id=self.user_info['id']
    #         )
    #     )
