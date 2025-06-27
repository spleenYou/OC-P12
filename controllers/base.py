class Controller:
    def __init__(self, ask, show, db, auth, session):
        self.session = session()
        self.auth = auth(self.session)
        self.db = db(self.session, self.auth)
        self.show = show(self.db, self.session)
        self.ask = ask(self.show, self.db, self.session)
        self.permissions = None

    def _check_token_and_perm(self):
        if self._has_user():
            if not self.auth.check_token():
                self.session.set_session(status='TOKEN', state='ERROR')
                return False
        if self._has_permission():
            self.session.set_session(status='FORBIDDEN', state='ERROR')
            return False
        return True

    def start(self, email):
        if not self._has_user():
            self.ask.wait()
            self.auth.generate_secret_key()
            self.session.connected_user.email = email
            self.session.user.department_id = 3
            self.session.set_session(status='ADD_USER')
            if not self.add('user'):
                self.session.set_session(state='ERROR', filter='STOPPED')
                self.ask.wait()
                return None
        self.session.set_session(status='CONNECTION')
        if not email:
            email = self.ask.email()
        password_in_db = self.db.get_user_password(email)
        if password_in_db is None:
            self.session.set_session(status='PASSWORD', filter='FIRST_TIME')
            self.ask.password()
            self.db.update_password_user(email)
            password_in_db = self.db.get_user_password(email)
        password = self.ask.password()
        if self.auth.check_password(password, password_in_db):
            self.session.connected_user = self.db.get_user_by_mail(email)
            self.permissions = self.session.connected_user.department.permissions
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
                    self._reset_password()
                else:
                    self.session.set_session(status=command[0])
            elif self._is_crud_command(command):
                self._make_filter(command)
                self.session.set_session(status='_'.join([command[0], command[1]]))
                if self._check_token_and_perm():
                    if self._is_in_db(command[1].lower()):
                        methods = {
                            'ADD': self.add,
                            'VIEW': self.view,
                            'DELETE': self.delete,
                        }
                        if command[0] in methods:
                            methods[command[0]](command[1].lower())
                        else:
                            eval('self.' + self.session.status.lower())()
                    else:
                        self.session.set_session('NO_' + command[1])
            else:
                self.session.set_session(status='UNKNOWN', state='ERROR')
            self.ask.wait()
            self.session.reset_session()
            if self.session.status == 'TOKEN':
                return None

    def _is_in_db(self, model):
        return self.db.number_of(model) > 0 or self.session.status.startswith('ADD')

    def add(self, model):
        self._fill_model(model)
        if self.ask.validation():
            if self.db.add(model):
                self.session.set_session(state='GOOD')
                return True
            else:
                self.session.set_session(state='ERROR')
        else:
            self.session.set_session(state='FAILED')
        return False

    def _fill_model(self, model):
        match model:
            case 'user':
                self.session.user.name = self.ask.name()
                if self.session.user.email is None:
                    self.session.user.email = self.ask.email()
                self.session.user.employee_number = self.ask.employee_number()
                if self.session.user.department_id is None:
                    self.session.user.department_id = self.ask.department()
            case 'client':
                self.session.client.company_name = self.ask.company_name()
                self.session.client.name = self.ask.client_name()
                self.session.client.email = self.ask.email()
                self.session.client.phone = self.ask.phone()
            case 'contract':
                self.ask.select('client')
                self.session.contract.total_amount = self.ask.total_amount()
                self.session.contract.rest_amount = self.ask.rest_amount()
            case 'event':
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

    def update_user(self):
        self.ask.select('user')
        savepoint = self.db.db_session.begin_nested()
        self.session.user.name = self.ask.name()
        self.session.user.email = self.ask.email()
        self.session.user.employee_number = self.ask.employee_number()
        self.session.user.department_id = self.ask.department()
        if self.ask.validation():
            self.session.set_session(state='GOOD')
            savepoint.commit()
            self.db.db_session.commit()
        else:
            self.session.set_session(state='FAILED')
            savepoint.rollback()

    def update_client(self):
        self.ask.select('client')
        savepoint = self.db.db_session.begin_nested()
        self.session.user = self.session.client.commercial_contact
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

    def update_event(self):
        self.ask.select('client')
        self.ask.select('contract')
        savepoint = self.db.db_session.begin_nested()
        if self.session.connected_user.department_id != 3:
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

    def view(self, model):
        if not self._for_all():
            self._fill_session(model)

    def delete(self, model):
        self._fill_session(model)
        if self.ask.validation():
            if self.db.delete(model):
                self.session.set_session(state='GOOD')
            else:
                self.session.set_session(state='ERROR')
        else:
            self.session.set_session(state='FAILED')

    def _fill_session(self, model):
        if model == 'user':
            self.ask.select('user')
        else:
            self.ask.select('client')
            if model != 'client':
                self.ask.select('contract')
                if model == 'event':
                    self.session.event = self.session.contract.event
            else:
                self.session.user = self.session.client.commercial_contact
        return None

    def _reset_password(self):
        if self.ask.validation():
            self.session.connected_user.password = None
            self.start(self.session.connected_user.email)

    def _for_all(self):
        return 'ALL' in self.session.filter

    def _stay(self, command):
        return command[0] not in ['exit', 'EXIT']

    def _make_filter(self, command):
        if command[0] == 'VIEW':
            filter = [c for c in command[2:]]
            self.session.set_session(filter='_'.join(filter))

    def _authorized_command(self, command):
        return command[0] in ['HELP', 'EXIT', 'PERMISSION', 'RESET']

    def _is_crud_command(self, command):
        return (command[0] in ['ADD', 'UPDATE', 'VIEW', 'DELETE'] and
                command[1] in ['USER', 'CLIENT', 'CONTRACT', 'EVENT'])

    def _has_user(self):
        return self.db.number_of('user') > 0

    def _has_permission(self):
        if self.permissions is None and self.session.status == 'ADD_USER':
            return False
        return (self.session.status[:4] != 'VIEW' and
                not getattr(self.permissions, self.session.status.lower()))
