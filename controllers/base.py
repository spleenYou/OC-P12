from copy import copy
from functools import wraps
from config import config


class Controller:
    def __init__(self, ask, show, db, auth, session):
        self.session = session()
        self.auth = auth(self.session)
        self.db = db(self.session, self.auth)
        self.show = show(self.db, self.session)
        self.ask = ask(self.show, self.db, self.session)
        self.permissions = None

    def check_token_and_perm(function):
        @wraps(function)
        def func_check(self, *args, **kwargs):
            if self.db.number_of_user() > 0:
                if not self.auth.check_token():
                    self.session.status = 'TOKEN'
                    self.session.state = 'ERROR'
                    return False
            if self.permissions is not None:
                if self.session.status[:4] != 'VIEW' and not getattr(self.permissions, self.session.status.lower()):
                    self.session.status = 'FORBIDDEN'
                    self.session.state = 'ERROR'
                    return False
            result = function(self, *args, **kwargs)
            return result
        return func_check

    def start(self, email):
        if self.db.number_of_user() == 0:
            self.ask.wait()
            self.auth.generate_secret_key()
            self.session.new_user.department_id = 3
            self.session.user.department_id = 3
            self.session.new_user.email = email
            self.session.status = 'ADD_USER'
            if not self.add_user():
                self.session.state = 'ERROR'
                self.session.filter = 'STOPPED'
                self.ask.wait()
                return None
        self.session.status = 'CONNECTION'
        self.session.user.email = self.ask.email(email)
        password_in_db = self.db.get_user_password()
        if password_in_db is None:
            self.session.filter = 'FIRST_TIME'
            self.session.status = 'PASSWORD'
            self.ask.password()
            self.db.update_password_user()
            password_in_db = self.db.get_user_password()
        self.session.status = 'CONNECTION'
        password = self.ask.password()
        if self.auth.check_password(password, password_in_db):
            self.session.user = self.db.get_user_by_mail(self.session.user.email)
            self.permissions = self.session.user.department.permissions
            self.auth.generate_token()
            self.session.state = 'GOOD'
            self.ask.wait()
            self.main_menu()
        else:
            self.session.state = 'FAILED'
            self.ask.wait()

    def main_menu(self):
        command = ['']
        while self._stay(command):
            self.session.state = 'NORMAL'
            self.session.status = 'MAIN_MENU'
            command = self.ask.command()
            command = command.upper().split(' ')
            if self._authorized_command(command):
                if len(command) > 1 and command[1] == 'PASSWORD':
                    self.reset_password()
                else:
                    self.session.status = command[0]
            elif self._authorized_crud_command(command):
                if self._command_possible(command):
                    self._make_filter(command)
                    command = '_'.join([command[0], command[1]])
                    self.session.status = command
                    eval('self.' + command.lower())()
                else:
                    self.session.status = 'NO_' + command[1]
            else:
                self.session.status = 'UNKNOWN'
                self.session.state = 'ERROR'
            self.ask.wait()
            self.session.reset_session()
            if self.session.status == 'TOKEN':
                self.ask.wait()
                self.start(None)

    @check_token_and_perm
    def add_user(self):
        self.session.new_user.name = self.ask.name()
        if self.session.new_user.email is None:
            self.session.new_user.email = self.ask.email()
        self.session.new_user.employee_number = self.ask.employee_number()
        if self.session.new_user.department_id is None:
            self.session.new_user.department_id = self.ask.department()
        if self.ask.validation():
            if self.db.add_user():
                self.session.state = 'GOOD'
                return True
            else:
                self.session.state = 'FAILED'
                return False

    @check_token_and_perm
    def update_user(self):
        self.select('user')
        savepoint = self.db.db_session.begin_nested()
        self.session.new_user.name = self.ask.name()
        self.session.new_user.email = self.ask.email()
        self.session.new_user.employee_number = self.ask.employee_number()
        self.session.new_user.department_id = self.ask.department()
        if self.ask.validation():
            self.session.state = 'GOOD'
            savepoint.commit()
            self.db.db_session.commit()
        else:
            self.session.state = 'FAILED'
            savepoint.rollback()

    @check_token_and_perm
    def view_user(self):
        if not self._for_all():
            self.select('user')

    @check_token_and_perm
    def delete_user(self):
        self.select('user')
        if self.ask.validation():
            self.session.state = 'GOOD'
            self.session.status = 'DELETE_USER'
            self.db.delete_user()

    @check_token_and_perm
    def add_client(self):
        self.session.new_user = copy(self.session.user)
        self.session.client.company_name = self.ask.company_name()
        self.session.client.name = self.ask.client_name()
        self.session.client.email = self.ask.email()
        self.session.client.phone = self.ask.phone()
        if self.ask.validation():
            if self.db.add_client():
                self.session.state = 'GOOD'
            else:
                self.session.state = 'FAILED'

    @check_token_and_perm
    def update_client(self):
        self.select('client')
        savepoint = self.db.db_session.begin_nested()
        self.session.new_user = self.session.client.commercial_contact
        self.session.client.company_name = self.ask.company_name()
        self.session.client.name = self.ask.client_name()
        self.session.client.email = self.ask.email()
        self.session.client.phone = self.ask.phone()
        if self.ask.validation():
            self.session.state = 'GOOD'
            savepoint.commit()
            self.db.db_session.commit()
        else:
            self.session.state = 'FAILED'
            savepoint.rollback()

    @check_token_and_perm
    def view_client(self):
        if not self._for_all():
            self.select('client')
            self.session.new_user = self.session.client.commercial_contact

    @check_token_and_perm
    def delete_client(self):
        self.select('client')
        self.session.new_user = self.session.client.commercial_contact
        if self.ask.validation():
            self.session.state = 'GOOD'
            self.db.delete_client()

    @check_token_and_perm
    def add_contract(self):
        self.select('client')
        self.session.contract.total_amount = self.ask.total_amount()
        self.session.contract.rest_amount = self.ask.rest_amount()
        if self.ask.validation():
            if self.db.add_contract():
                self.session.state = 'GOOD'
            else:
                self.session.state = 'FAILED'

    @check_token_and_perm
    def update_contract(self):
        self.select('client')
        self.select('contract')
        savepoint = self.db.db_session.begin_nested()
        self.session.contract.total_amount = self.ask.total_amount()
        self.session.contract.rest_amount = self.ask.rest_amount()
        self.session.contract.status = self.ask.status()
        if self.ask.validation():
            self.session.state = 'GOOD'
            savepoint.commit()
            self.db.db_session.commit()
        else:
            self.session.state = 'FAILED'
            savepoint.rollback()

    @check_token_and_perm
    def delete_contract(self):
        self.select('client')
        self.select('contract')
        if self.ask.validation():
            if self.db.delete_contract():
                self.session.state = 'GOOD'
            else:
                self.session.state = 'FAILED'

    @check_token_and_perm
    def view_contract(self):
        if not self._for_all():
            filter = self.session.filter
            self.select('client')
            self.session.filter = filter
            self.select('contract')

    @check_token_and_perm
    def add_event(self):
        if len(self.db.get_client_list()) > 0:
            self.select('client')
            self.select('contract')
            self.session.event.location = self.ask.location()
            self.session.event.attendees = self.ask.attendees()
            self.session.event.date_start = self.ask.date_start()
            self.session.event.date_stop = self.ask.date_stop()
            self.session.event.notes = self.ask.notes()
            self.session.filter = 'SUPPORT'
            if self.db.number_of_user() > 0:
                self.select('support')
            validation = self.ask.validation()
            if validation:
                if self.db.add_event():
                    self.session.state = 'GOOD'
                else:
                    self.session.state = 'ERROR'
            else:
                self.db.db_session.rollback()
                self.session.state = 'FAILED'
        else:
            self.session.status = 'NO_CLIENT'
            self.session.state = 'WITHOUT_EVENT'

    @check_token_and_perm
    def update_event(self):
        self.select('client')
        self.select('contract')
        savepoint = self.db.db_session.begin_nested()
        if self.session.user.department_id != 3:
            self.session.contract.event.location = self.ask.location()
            self.session.contract.event.attendees = self.ask.attendees()
            self.session.contract.event.date_start = self.ask.date_start()
            self.session.contract.event.date_stop = self.ask.date_stop()
            self.session.contract.event.notes = self.ask.notes()
        self.select('support')
        if self.ask.validation():
            self.session.state = 'GOOD'
            savepoint.commit()
            self.db.db_session.commit()
        else:
            self.session.state = 'FAILED'
            savepoint.rollback()

    @check_token_and_perm
    def delete_event(self):
        self.select('client')
        self.select('contract')
        if self.ask.validation():
            if self.db.delete_event():
                self.session.state = 'GOOD'
            else:
                self.session.state = 'FAILED'

    @check_token_and_perm
    def view_event(self):
        if not self._for_all():
            self.select('client')
            self.select('contract')

    def reset_password(self):
        if self.ask.validation():
            self.session.user.password = None
            self.start(self.session.user.email)

    def select(self, model):
        number = None
        previous_filter = self.session.filter
        previous_status = self.session.status
        self.session.status = config.select_status[model]
        while number is None:
            self.session.state = 'NORMAL'
            self._set_filter(previous_status, previous_filter)
            number = self.ask._prompt(model)
            try:
                number = int(number)
                number_methods = {
                    'user': self.db.number_of_user,
                    'support': self.db.number_of_user,
                    'client': self.db.number_of_client,
                    'contract': self.db.number_of_contract,
                }
                if number < number_methods[model]():
                    self._set_session_model(model, number)
                    self.session.filter = previous_filter
                    self.session.status = previous_status
                    return None
                else:
                    self.session.state = 'FAILED'
            except Exception:
                self.session.state = 'ERROR'
            number = None
            self.ask.wait()

    def _for_all(self):
        return 'ALL' in self.session.filter

    def _stay(self, command):
        return command[0] not in ['exit', 'EXIT']

    def _make_filter(self, command):
        if command[0] == 'VIEW':
            filter = [c for c in command[2:]]
            self.session.filter = '_'.join(filter)

    def _set_filter(self, status, previous_filter):
        if status in ['UPDATE_CONTRACT', 'DELETE_CONTRACT', 'VIEW_CONTRACT']:
            self.session.filter = 'WITH_CONTRACT'
        elif status == 'ADD_EVENT' and previous_filter != 'SUPPORT':
            self.session.filter = 'WITHOUT_EVENT'
        elif status in ['UPDATE_EVENT', 'DELETE_EVENT', 'VIEW_EVENT']:
            self.session.filter = 'WITH_EVENT'
        elif status == 'DELETE_USER':
            self.session.filter = 'FOR_DELETE'

    def _command_possible(self, command):
        return (command[0] == 'ADD' or
                (command[0] != 'ADD' and eval('self.db.number_of_' + command[1].lower())() > 0))

    def _authorized_command(self, command):
        return command[0] in ['HELP', 'EXIT', 'PERMISSION', 'RESET']

    def _authorized_crud_command(self, command):
        return (command[0] in ['ADD', 'UPDATE', 'VIEW', 'DELETE'] and
                command[1] in ['USER', 'CLIENT', 'CONTRACT', 'EVENT'])

    def _set_session_model(self, model, number):
        get_methods = {
            'user': self.db.get_user_by_number,
            'client': self.db.get_client,
            'contract': self.db.get_contract,
            'support': self.db.get_user_by_number,
        }
        session_attributes = {
            'user': 'new_user',
            'support': 'new_user',
            'client': 'client',
            'contract': 'contract'
        }
        result = get_methods[model](number)
        setattr(self.session, session_attributes[model], result)
