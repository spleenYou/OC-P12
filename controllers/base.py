from copy import copy
from functools import wraps


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
            if self._has_user():
                if not self.auth.check_token():
                    self.session.set_session(status='TOKEN', state='ERROR')
                    return False
            if self._has_permission():
                self.session.set_session(status='FORBIDDEN', state='ERROR')
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
            self.session.set_session('ADD_USER')
            if not self.add_user():
                self.session.set_session(state='ERROR', filter='STOPPED')
                self.ask.wait()
                return None
        self.session.set_session(status='CONNECTION')
        self.session.user.email = self.ask.email(email)
        password_in_db = self.db.get_user_password()
        if password_in_db is None:
            self.session.set_session(status='PASSWORD', filter='FIRST_TIME')
            self.ask.password()
            self.db.update_password_user()
            password_in_db = self.db.get_user_password()
        password = self.ask.password()
        if self.auth.check_password(password, password_in_db):
            self.session.user = self.db.get_user_by_mail(self.session.user.email)
            self.permissions = self.session.user.department.permissions
            self.auth.generate_token()
            self.session.set_session(state='GOOD')
            self.ask.wait()
            self.main_menu()
        else:
            self.session.set_session(state='FAILED')
            self.ask.wait()

    def main_menu(self):
        command = ['']
        while self._stay(command):
            self.session.set_session(status='MAIN_MENU', state='NORMAL')
            command = self.ask.command()
            command = command.upper().split(' ')
            if self._authorized_command(command):
                if len(command) > 1 and command[1] == 'PASSWORD':
                    self.reset_password()
                else:
                    self.session.set_session(status=command[0])
            elif self._authorized_crud_command(command):
                if self._command_possible(command):
                    self._make_filter(command)
                    command = '_'.join([command[0], command[1]])
                    self.session.set_session(status=command)
                    eval('self.' + command.lower())()
                else:
                    self.session.set_session('NO_' + command[1])
            else:
                self.session.set_session(status='UNKNOWN', state='ERROR')
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
                self.session.set_session(state='GOOD')
                return True
            else:
                self.session.set_session(state='FAILED')
                return False

    @check_token_and_perm
    def update_user(self):
        self.ask.select('user')
        savepoint = self.db.db_session.begin_nested()
        self.session.new_user.name = self.ask.name()
        self.session.new_user.email = self.ask.email()
        self.session.new_user.employee_number = self.ask.employee_number()
        self.session.new_user.department_id = self.ask.department()
        if self.ask.validation():
            self.session.set_session(state='GOOD')
            savepoint.commit()
            self.db.db_session.commit()
        else:
            self.session.set_session(state='FAILED')
            savepoint.rollback()

    @check_token_and_perm
    def view_user(self):
        if not self._for_all():
            self.ask.select('user')

    @check_token_and_perm
    def delete_user(self):
        self.ask.select('user')
        if self.ask.validation():
            self.session.set_session(state='GOOD')
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
                self.session.set_session(state='GOOD')
            else:
                self.session.set_session(state='FAILED')

    @check_token_and_perm
    def update_client(self):
        self.ask.select('client')
        savepoint = self.db.db_session.begin_nested()
        self.session.new_user = self.session.client.commercial_contact
        self.session.client.company_name = self.ask.company_name()
        self.session.client.name = self.ask.client_name()
        self.session.client.email = self.ask.client_email()
        self.session.client.phone = self.ask.phone()
        if self.ask.validation():
            self.session.set_session(state='GOOD')
            savepoint.commit()
            self.db.db_session.commit()
        else:
            self.session.set_session(state='FAILED')
            savepoint.rollback()

    @check_token_and_perm
    def view_client(self):
        if not self._for_all():
            self.ask.select('client')
            self.session.new_user = self.session.client.commercial_contact

    @check_token_and_perm
    def delete_client(self):
        self.ask.select('client')
        self.session.new_user = self.session.client.commercial_contact
        if self.ask.validation():
            self.session.set_session(state='GOOD')
            self.db.delete_client()

    @check_token_and_perm
    def add_contract(self):
        self.ask.select('client')
        self.session.contract.total_amount = self.ask.total_amount()
        self.session.contract.rest_amount = self.ask.rest_amount()
        if self.ask.validation():
            if self.db.add_contract():
                self.session.set_session(state='GOOD')
            else:
                self.session.set_session(state='FAILED')

    @check_token_and_perm
    def update_contract(self):
        self.ask.select('client')
        self.ask.select('contract')
        savepoint = self.db.db_session.begin_nested()
        self.session.contract.total_amount = self.ask.total_amount()
        self.session.contract.rest_amount = self.ask.rest_amount()
        self.session.contract.status = self.ask.status()
        if self.ask.validation():
            self.session.set_session(state='GOOD')
            savepoint.commit()
            self.db.db_session.commit()
        else:
            self.session.set_session(state='FAILED')
            savepoint.rollback()

    @check_token_and_perm
    def delete_contract(self):
        self.ask.select('client')
        self.ask.select('contract')
        if self.ask.validation():
            if self.db.delete_contract():
                self.session.set_session(state='GOOD')
            else:
                self.session.set_session(state='FAILED')

    @check_token_and_perm
    def view_contract(self):
        if not self._for_all():
            filter = self.session.filter
            self.ask.select('client')
            self.session.set_session(filter=filter)
            self.ask.select('contract')

    @check_token_and_perm
    def add_event(self):
        if len(self.db.get_client_list()) > 0:
            self.ask.select('client')
            self.ask.select('contract')
            self.session.event.location = self.ask.location()
            self.session.event.attendees = self.ask.attendees()
            self.session.event.date_start = self.ask.date_start()
            self.session.event.date_stop = self.ask.date_stop()
            self.session.event.notes = self.ask.notes()
            self.session.set_session(filter='SUPPORT')
            if self._has_user():
                self.ask.select('support')
            validation = self.ask.validation()
            if validation:
                if self.db.add_event():
                    self.session.set_session(state='GOOD')
                else:
                    self.session.set_session(state='ERROR')
            else:
                self.db.db_session.rollback()
                self.session.set_session(state='FAILED')
        else:
            self.session.set_session(status='NO_CLIENT', state='WITHOUT_EVENT')

    @check_token_and_perm
    def update_event(self):
        self.ask.select('client')
        self.ask.select('contract')
        savepoint = self.db.db_session.begin_nested()
        if self.session.user.department_id != 3:
            self.session.contract.event.location = self.ask.location()
            self.session.contract.event.attendees = self.ask.attendees()
            self.session.contract.event.date_start = self.ask.date_start()
            self.session.contract.event.date_stop = self.ask.date_stop()
            self.session.contract.event.notes = self.ask.notes()
        self.session.set_session(filter='SUPPORT')
        if self._has_user():
            self.ask.select('support')
        if self.ask.validation():
            self.session.set_session(state='GOOD')
            savepoint.commit()
            self.db.db_session.commit()
        else:
            self.session.set_session(state='FAILED')
            savepoint.rollback()

    @check_token_and_perm
    def delete_event(self):
        self.ask.select('client')
        self.ask.select('contract')
        if self.ask.validation():
            if self.db.delete_event():
                self.session.set_session(state='GOOD')
            else:
                self.session.set_session(state='FAILED')

    @check_token_and_perm
    def view_event(self):
        if not self._for_all():
            self.ask.select('client')
            self.ask.select('contract')

    def reset_password(self):
        if self.ask.validation():
            self.session.user.password = None
            self.start(self.session.user.email)

    def _for_all(self):
        return 'ALL' in self.session.filter

    def _stay(self, command):
        return command[0] not in ['exit', 'EXIT']

    def _make_filter(self, command):
        if command[0] == 'VIEW':
            filter = [c for c in command[2:]]
            self.session.set_session(filter='_'.join(filter))

    def _command_possible(self, command):
        return (command[0] == 'ADD' or
                (command[0] != 'ADD' and eval('self.db.number_of_' + command[1].lower())() > 0))

    def _authorized_command(self, command):
        return command[0] in ['HELP', 'EXIT', 'PERMISSION', 'RESET']

    def _authorized_crud_command(self, command):
        return (command[0] in ['ADD', 'UPDATE', 'VIEW', 'DELETE'] and
                command[1] in ['USER', 'CLIENT', 'CONTRACT', 'EVENT'])

    def _has_user(self):
        return self.db.number_of_user() > 0

    def _has_permission(self):
        if self.permissions is None and self.session.status == 'ADD_USER':
            return False
        return (self.session.status[:4] != 'VIEW' and
                not getattr(self.permissions, self.session.status.lower()))
