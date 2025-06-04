from controllers.permissions import Check_Permission
from functools import wraps


class Controller:
    def __init__(self, prompt, show, db, auth):
        self.prompt = prompt()
        self.show = show()
        self.db = db()
        self.user_info = None
        get_perms = self.db.get_permissions()
        self.allows_to = Check_Permission(get_perms)
        self.auth = auth()
        self.first_launch = True
        self.client = None

    def check_token_and_permission(function):
        @wraps(function)
        def func_check(self, *args, **kwargs):
            if not (self.first_launch or self.auth.check_token()):
                print(f'token : {self.auth.check_token()}')
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
            self.user_info.department_id = 3
            self.add_user()
        self.first_launch = False
        password = self.prompt.for_password()
        self.user_info = self.db.check_user_login(self.user_info.email, password)
        if self.user_info:
            self.auth.generate_token(self.user_info.department_id)
            self.show.logged_ok()
        else:
            self.show.logged_nok()

    @check_token_and_permission
    def add_user(self):
        if self.allows_to.add_user(self.user_info.department_id):
            name = self.prompt.for_name()
            email = self.user_info.email
            department_id = self.user_info.department_id
            if not self.first_launch:
                email = self.prompt.for_email()
                department_id = self.prompt.for_department(self.db.get_department_list())
            password = self.prompt.for_password()
            employee_number = self.prompt.for_employee_number()
            result = self.db.add_epic_user(name, email, password, employee_number, department_id)
            return result
        return False

    @check_token_and_permission
    def add_client(self):
        if self.allows_to.add_client(self.user_info.department_id):
            name = self.prompt.for_client_name()
            email = self.prompt.for_email()
            phone = self.prompt.for_phone()
            entreprise_name = self.prompt.for_entreprise_name()
            result = self.db.add_client(
                name=name,
                email=email,
                phone=phone,
                entreprise_name=entreprise_name,
                commercial_contact_id=self.user_info.id
            )
            return result
        print(f'Add client not allowed {self.user_info.department_id}')
        return False

    @check_token_and_permission
    def add_contract(self):
        if self.allows_to.add_contract(self.user_info.department_id):
            if self.client is None:
                pass  # Todo when select_client() created
            total_amount = self.prompt.for_total_amount()
            rest_amount = self.prompt.for_rest_amount()
            print(self.client.commercial_contact_id)
            print(self.client)
            result = self.db.add_contract(
                client_id=self.client.id,
                commercial_id=self.client.commercial_contact_id,
                total_amount=total_amount,
                rest_amount=rest_amount
            )
            return result
        print('Add contract not allowed')
        return False
