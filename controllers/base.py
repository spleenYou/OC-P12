import re
from controllers.permissions import Permission
from functools import wraps


class Controller:
    def __init__(self, prompt, show, db, auth, session):
        self.session = session
        self.auth = auth(session)
        self.db = db(session, self.auth)
        self.show = show(self.db, session)
        self.prompt = prompt(self.show)
        self.allows_to = Permission(self.db, session)
        self.email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    def check_token_and_perm(function):
        @wraps(function)
        def func_check(self, *args, **kwargs):
            if not (self.session.status == 'FIRST_LAUNCH' or self.auth.check_token()):
                return False
            return function(self, *args, **kwargs)
            if eval('self.allows_to.' + function.__name__)():
                return False
        return func_check

    def start(self, email):
        if self.db.number_of_users() == 0:
            self.session.status = 'FIRST_LAUNCH'
            self.show.wait()
            self.auth.generate_secret_key()
            self.session.new_user['department_id'] = 3
            self.session.new_user['email'] = email
            if not self.add_user():
                self.show.wait()
                return None
            self.show.wait()
        self.session.status = 'CONNECTION'
        self.session.user["email"] = self.ask_email(email)
        password = self.prompt.for_password()
        if self.auth.check_password(password, self.db.get_user_password()):
            user_id = self.db.get_user_id(self.session.user["email"])
            self.session.user = self.db.get_user_information(user_id)
            self.auth.generate_token()
            self.session.status = 'LOGIN_OK'
        else:
            self.session.status = 'LOGIN_FAILED'
        self.show.wait()
        return None

    def main_menu(self):
        command = ['']
        while command[0] not in ['exit', 'EXIT']:
            self.session.status = 'MAIN_MENU'
            command = self.prompt.for_command()
            command = command.upper().split(' ')
            if command[0] in ['HELP', 'EXIT']:
                self.session.status = command[0]
            elif (command[0] in ['ADD', 'UPDATE', 'DELETE'] and
                    command[1] in ['user', 'USER', 'client', 'CLIENT', 'contract', 'CONTRACT', 'event', 'EVENT']):
                command = command[0] + '_' + command[1]
                self.session.status = command
                eval('self.' + command.lower())()
            else:
                self.session.status = 'UNKNOWN'
            self.show.wait()

    def ask_name(self):
        name = self.prompt.for_name()
        if name == '':
            name = self.session.new_user['name']
        return name

    def ask_email(self, email=None):
        status = self.session.status
        while email is None:
            self.session.status = status
            email = self.prompt.for_email()
            if status == 'UPDATE_USER' and email == '':
                email = self.session.new_user['email']
            elif not re.fullmatch(self.email_regex, email or ''):
                email = None
                self.session.status = 'BAD_EMAIL'
                self.show.wait()
        return email

    def ask_employee_number(self):
        status = self.session.status
        employee_number = None
        while employee_number is None:
            self.session.status = status
            employee_number = self.prompt.for_employee_number()
            if status == 'UPDATE_USER' and employee_number == '':
                return self.session.new_user['employee_number']
            try:
                employee_number = int(employee_number)
            except Exception:
                employee_number = None
                self.session.status = 'BAD_EMPLOYEE_NUMBER'
                self.show.wait()
        return employee_number

    def ask_password(self):
        status = self.session.status
        password = None
        while password is None:
            self.session.status = status
            password = self.prompt.for_password()
            if status == 'UPDATE_USER' and password == '':
                password = self.session.new_user['password']
            elif password == '':
                password = None
                self.session.status = 'EMPTY_PASSWORD'
                self.show.wait()
        return password

    def ask_department(self):
        status = self.session.status
        department_id = None
        if status != 'UPDATE_USER':
            department_id = self.session.new_user['department_id']
        department_list = self.db.get_department_list()
        while department_id is None:
            self.session.status = status
            department_id = self.prompt.for_department(department_list)
            if status == 'UPDATE_USER' and department_id == '':
                return self.session.new_user['department_id']
            try:
                department_id = int(department_id)
            except Exception:
                department_id = None
                self.session.status = 'BAD_DEPARTMENT'
                self.show.wait()
        return department_id

    @check_token_and_perm
    def add_user(self):
        self.session.status = 'ADD_USER'
        self.session.new_user['name'] = self.ask_name()
        if self.session.new_user['email'] is None:
            self.session.new_user['email'] = self.ask_email()
        self.session.new_user['password'] = self.ask_password()
        self.session.new_user['employee_number'] = self.ask_employee_number()
        if self.session.new_user['department_id'] is None:
            self.session.new_user['department_id'] = self.ask_department()
        if self.prompt.for_validation():
            if self.db.add_user():
                self.session.reset_new_user()
                self.session.status = 'ADD_USER_OK'
                return True
        self.session.status = 'ADD_USER_FAILED'
        return False

    @check_token_and_perm
    def update_user(self):
        user_id = self.select_user()
        self.session.new_user = self.db.get_user_information(user_id)
        self.session.new_user['name'] = self.ask_name()
        self.session.new_user['email'] = self.ask_email()
        self.session.new_user['password'] = self.ask_password()
        self.session.new_user['employee_number'] = self.ask_employee_number()
        self.session.new_user['department_id'] = self.ask_department()
        if self.prompt.for_validation():
            self.session.status = 'UPDATE_USER_OK'
            self.db.update_user()

    def select_user(self):
        number = None
        while number is None:
            self.session.status = 'SELECT_USER'
            number = self.prompt.for_user()
            try:
                number = int(number)
                if number < self.db.number_of_users():
                    user_id = self.db.find_user_id(number)
                    self.session.status = 'UPDATE_USER'
                    return user_id
                else:
                    self.session.status = 'SELECT_USER_FAILED'
            except Exception:
                self.session.status = 'BAD_SELECT_USER'
            number = None
            self.show.wait()

    @check_token_and_perm
    def add_client(self):
        name = self.prompt.for_client_name()
        email = self.prompt.for_email()
        phone = self.prompt.for_phone()
        entreprise_name = self.prompt.for_entreprise_name()
        result = self.db.add_client(
            name=name,
            email=email,
            phone=phone,
            entreprise_name=entreprise_name,
            commercial_contact_id=self.user.id
        )
        return result
        print(f'Add client not allowed {self.user.department_id}')

    def select_client(self):
        client_list = self.db.get_client_list()
        client = self.prompt.for_select_client(client_list)
        if client is not None:
            return client
        return None

    @check_token_and_perm
    def add_contract(self):
        if self.allows_to.add_contract(self.user.department_id):
            if self.client is None:
                self.client = self.select_client()
            if self.client is not None:
                total_amount = self.prompt.for_total_amount()
                rest_amount = self.prompt.for_rest_amount()
                result = self.db.add_contract(
                    client_id=self.client.id,
                    commercial_id=self.client.commercial_contact_id,
                    total_amount=total_amount,
                    rest_amount=rest_amount
                )
                return result
            print('Add contract canceled')
            return False
        print('Add contract not allowed')
        return False
