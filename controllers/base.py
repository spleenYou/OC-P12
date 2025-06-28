from config import config


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
        if not self._has_permission():
            self.session.set_session(status='FORBIDDEN', state='ERROR')
            return False
        return True

    def start(self, email):
        if not self._has_user():
            self.ask.wait()
            self.session.set_session(status='ADD_USER', filter='FIRST_TIME')
            if not self._execute_crud():
                self.session.set_session(state='ERROR', filter='STOPPED')
                self.ask.wait()
                return None
            self.auth.generate_secret_key()
        self.session.set_session(status='CONNECTION')
        if not email:
            email = self.ask.email()
        password_in_db = self._find_password_in_db(email)
        password = self.ask.password()
        if self.auth.check_password(password, password_in_db):
            self._prepare_session(email)
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
                self.session.set_session(status='_'.join([command[0], command[1]]))
                if self._check_token_and_perm():
                    if self._is_in_db(command[1].lower()):
                        self._make_filter(command)
                        self._execute_crud()
                    else:
                        self.session.set_session('NO_' + command[1])
            else:
                self.session.set_session(status='UNKNOWN', state='ERROR')
            self.ask.wait()
            self.session.reset_session()
            if self.session.status == 'TOKEN':
                return None

    def _execute_crud(self):
        action, model = self.session.status.lower().split('_')
        self._fill_session(model)
        if action in ['add', 'update']:
            if action == 'update':
                savepoint = self._save_model(model)
            self._fill_model(model)
        if action != 'view':
            validation = self.ask.validation()
        else:
            validation = True
        if validation:
            if self._execute_command(action, model):
                self.session.set_session(state='GOOD')
                return True
            else:
                self.session.set_session(state='ERROR')
                validation = False
        else:
            self.session.set_session(state='FAILED')
        if action == 'update':
            self._restore_model(model, savepoint)
        return False

    def _save_model(self, model):
        save = {}
        model_to_save = getattr(self.session, model)
        for attr in getattr(config, model + '_attrs'):
            save[attr] = getattr(model_to_save, attr)
        return save

    def _restore_model(self, model, save):
        model_to_restore = getattr(self.session, model)
        for attr in getattr(config, model + '_attrs'):
            setattr(model_to_restore, attr, save[attr])

    def _execute_command(self, action, model):
        match action:
            case 'add':
                return self.db.add(model)
            case 'update':
                return True
            case 'view':
                return True
            case 'delete':
                return self.db.delete(model)

    def _is_in_db(self, model):
        return self.db.number_of(model) > 0 or self.session.status.startswith('ADD')

    def _fill_model(self, model):
        match model:
            case 'user':
                self.session.user.name = self.ask.name()
                self.session.user.email = self.ask.email()
                self.session.user.employee_number = self.ask.employee_number()
                if self.session.filter == 'FIRST_TIME':
                    self.session.user.department_id = 3
                else:
                    self.session.user.department_id = self.ask.department()
            case 'client':
                self.session.client.company_name = self.ask.company_name()
                self.session.client.name = self.ask.client_name()
                self.session.client.email = self.ask.client_email()
                self.session.client.phone = self.ask.phone()
            case 'contract':
                self.session.contract.total_amount = self.ask.total_amount()
                self.session.contract.rest_amount = self.ask.rest_amount()
                if self.session.status.startswith('UPDATE'):
                    self.session.contract.status = self.ask.status()
            case 'event':
                if self.session.connected_user.department_id != 3:
                    self.session.event.location = self.ask.location()
                    self.session.event.attendees = self.ask.attendees()
                    self.session.event.date_start = self.ask.date_start()
                    self.session.event.date_stop = self.ask.date_stop()
                    self.session.event.notes = self.ask.notes()
                self.session.set_session(filter='SUPPORT')
                if self._has_user():
                    self.ask.select('support')

    def _fill_session(self, model):
        if self.session.status.startswith('VIEW') and self._for_all():
            return None
        if model == 'user':
            if not self.session.status.startswith('ADD'):
                self.ask.select('user')
        elif not (model == 'client' and self.session.status.startswith('ADD')):
            self.ask.select('client')
            if model != 'client':
                if not (model == 'contract' and self.session.status.startswith('ADD')):
                    self.ask.select('contract')
                    if model == 'event' and self.session.contract.event:
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
            return True
        return (self.session.status.startswith('VIEW') or
                getattr(self.permissions, self.session.status.lower()))

    def _find_password_in_db(self, email):
        password = self.db.get_user_password(email)
        if password is None:
            self._define_password(email)
            password = self.db.get_user_password(email)
        return password

    def _define_password(self, email):
        self.session.set_session(status='PASSWORD', filter='FIRST_TIME')
        self.ask.password()
        self.db.update_password_user(email)

    def _prepare_session(self, email):
        self.session.connected_user = self.db.get_user_by_mail(email)
        self.permissions = self.session.connected_user.department.permissions
        self.auth.generate_token()
        self.session.set_session(state='GOOD')
        self.ask.wait()
