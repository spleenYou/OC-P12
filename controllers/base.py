from controllers.permissions import Check_Permission


class Controller:
    def __init__(self, prompt, show, db, auth):
        self.prompt = prompt()
        self.show = show()
        self.db = db()
        self.user_info = None
        get_perms = self.db.get_permissions()
        self.allows_to = Check_Permission(get_perms)
        self.auth = auth()

    def check_token(function):

        def func_check(self, *args, **kwargs):
            if not self.auth.check_token():
                return False
            return function(self, *args, **kwargs)
        return func_check

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

    @check_token
    def add_user(self, ask_email=None, department_id=None):
        if self.allows_to.add_user(self.user_info.department_id):
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
                pass
                # Show a message if not
        return False

    @check_token
    def add_client(self):
        if self.allows_to.add_user(self.user_info.department_id):
            name = self.prompt.for_client_name()
            email = self.prompt.for_email()
            phone = self.prompt.for_phone()
            entreprise_name = self.prompt.for_entreprise_name()
            return self.db.add_client(
                name=name,
                email=email,
                phone=phone,
                entreprise_name=entreprise_name,
                commercial_contact_id=self.user_info.id
            )
        return False
