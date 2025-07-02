import os
from config import config


class Controller:
    def __init__(self, ask, show, db, auth, session):
        self.session = session()
        self.auth = auth(self.session)
        self.db = db(self.session, self.auth)
        self.show = show(self.db, self.session)
        self.ask = ask(self.show, self.db, self.session)
        self.permissions = None
        self._has_user = False

    def _check_token_and_perm(self):
        if self._has_user:
            if not self.auth.check_token():
                self.session.set_session(action='TOKEN', state='ERROR', user_cmd='')
                return False
        if not self._has_permission():
            self.session.set_session(action='FORBIDDEN', state='ERROR', user_cmd='')
            return False
        return True

    def start(self, email):
        self.session.action = 'FIRST_LAUNCH'
        if not self._user_in_db():
            self.ask.wait()
            self.session.set_session(action='ADD', model='USER', filter='FIRST_TIME')
            if not self._execute_crud():
                self.session.set_session(state='FAILED', model='STOPPED')
                self.ask.wait()
                return None
            self.auth.generate_secret_key()
            self.ask.wait()
        self._has_user = True
        self.session.reset_session()
        self.session.set_session(action='CONNECTION')
        if not email:
            email = self.ask.email()
        password_in_db = self._find_password_in_db(email)
        password = self.ask.password()
        if self.auth.check_password(password, password_in_db):
            self._prepare_session(email)
            self.ask.wait()
            self.main_menu()
        else:
            self.session.set_session(state='FAILED')
            self.ask.wait()

    def main_menu(self):
        while True:
            self.session.set_session(action='MAIN_MENU', state='NORMAL')
            user_input = self.ask.command().upper()
            self._set_session(user_input)
            if self._authorized_action():
                if self.session.model == 'PASSWORD':
                    self._reset_password()
            elif self._is_crud_command():
                if self._check_token_and_perm():
                    if self._check_possibility():
                        self._execute_crud()
                    else:
                        self.session.set_session(action='NO_' + self.session.model, user_cmd='')
            else:
                self.session.set_session(action='UNKNOWN', state='ERROR')
            self.ask.wait()
            if self._stop_app():
                os._exit(os.EX_OK)
            self.session.reset_session()

    def _check_possibility(self):
        if self.session.action == 'ADD':
            if self.session.model in ['USER', 'CLIENT']:
                return True
            elif self.session.model == 'CONTRACT':
                return self.db.number_of('CLIENT')
            else:
                self.session.set_session(filter='WITHOUT_EVENT')
                return self.db.number_of('CONTRACT') > 0
        else:
            return self.db.number_of(self.session.model) > 0

    def _execute_crud(self):
        if self.session.filter != 'FIRST_TIME':
            self._fill_session()
        if self.session.action == 'VIEW':
            return None
        if self.session.action in ['ADD', 'UPDATE']:
            if self.session.action == 'UPDATE':
                savepoint = self._save_model()
            self._fill_model()
        if self.ask.validation():
            if self._execute_command():
                self.session.set_session(state='GOOD')
                self.db.db_session.commit()
                return True
            else:
                self.session.set_session(state='ERROR')
        else:
            self.session.set_session(state='FAILED')
        if self.session.action == 'UPDATE':
            self._restore_model(savepoint)
            self.db.db_session.commit()
        return False

    def _save_model(self):
        save = {}
        model_to_save = getattr(self.session, self.session.model.lower())
        for attr in getattr(config, self.session.model.lower() + '_attrs'):
            save[attr] = getattr(model_to_save, attr)
        return save

    def _restore_model(self, save):
        model_to_restore = getattr(self.session, self.session.model.lower())
        for attr in getattr(config, self.session.model.lower() + '_attrs'):
            setattr(model_to_restore, attr, save[attr])

    def _execute_command(self):
        match self.session.action:
            case 'ADD':
                return self.db.add()
            case 'UPDATE':
                return True
            case 'VIEW':
                return True
            case 'DELETE':
                return self.db.delete()

    def _fill_model(self):
        match self.session.model:
            case 'USER':
                self.session.user.name = self.ask.name()
                self.session.user.email = self.ask.email()
                self.session.user.employee_number = self.ask.employee_number()
                if self.session.filter == 'FIRST_TIME':
                    self.session.user.department_id = 3
                else:
                    self.session.user.department_id = self.ask.department()
            case 'CLIENT':
                self.session.client.company_name = self.ask.company_name()
                self.session.client.name = self.ask.client_name()
                self.session.client.email = self.ask.client_email()
                self.session.client.phone = self.ask.phone()
            case 'CONTRACT':
                self.session.contract.total_amount = self.ask.total_amount()
                self.session.contract.rest_amount = self.ask.rest_amount()
                if self.session.action == 'UPDATE':
                    self.session.contract.status = self.ask.status()
            case 'EVENT':
                if self.session.connected_user.department_id != 3:
                    self.session.event.location = self.ask.location()
                    self.session.event.attendees = self.ask.attendees()
                    self.session.event.date_start = self.ask.date_start()
                    self.session.event.date_stop = self.ask.date_stop()
                    self.session.event.notes = self.ask.notes()
                self.session.set_session(filter='SUPPORT')
                if self._user_in_db():
                    self.ask.select('USER')
                    if self.session.action == 'UPDATE':
                        self.session.event.support_contact_id = self.session.user.id
                        self.db.db_session.commit()

    def _fill_session(self):
        if self.session.action == 'VIEW':
            if self._want_all():
                return None
        if self.session.model == 'USER':
            if not self.session.action == 'ADD':
                self.ask.select('USER')
        elif not (self.session.model == 'CLIENT' and self.session.action == 'ADD'):
            self.ask.select('CLIENT')
            if self.session.model != 'CLIENT':
                if not (self.session.model == 'CONTRACT' and self.session.action == 'ADD'):
                    self.ask.select('CONTRACT')
                    if self.session.model == 'EVENT' and self.session.contract.event:
                        self.session.event = self.session.contract.event
                else:
                    self.session.user = self.session.client.commercial_contact
        return None

    def _reset_password(self):
        self.session.set_session(state='ERROR')
        if self.ask.validation():
            self.session.connected_user.password = None
            self.db.db_session.commit()
            self.start(self.session.connected_user.email)
        else:
            self.session.set_session(state='FAILED')

    def _stop_app(self):
        return self.session.user_cmd.startswith(('exit', 'EXIT')) or self.session.action == 'TOKEN'

    def _authorized_action(self):
        return (self.session.action in config.authorized_action and
                self.session.model in ['', 'PASSWORD'])

    def _is_crud_command(self):
        return (self.session.action in config.crud_action and
                self.session.model in config.app_model)

    def _user_in_db(self):
        return self.db.number_of('USER') > 0

    def _has_permission(self):
        if self.permissions is None and self.session.action == 'ADD':
            return True
        return (self.session.action == 'VIEW' or
                getattr(self.permissions, self.session.user_cmd.lower()))

    def _find_password_in_db(self, email):
        password = self.db.get_user_password(email)
        if password is None:
            self._define_password(email)
            password = self.db.get_user_password(email)
        return password

    def _define_password(self, email):
        self.session.set_session(action='PASSWORD', filter='FIRST_TIME')
        self.ask.password()
        self.db.update_password_user(email)

    def _prepare_session(self, email):
        self.session.set_session(state='GOOD', filter='EMAIL')
        self.session.connected_user.email = email
        self.session.connected_user = self.db.get('USER', 0)
        self.permissions = self.session.connected_user.department.permissions
        self.auth.generate_token()

    def _set_session(self, user_input):
        model = None
        parsed = user_input.split(' ')
        parsed = self._set_for_all(parsed)
        if len(parsed) > 1:
            model = parsed[1]
        filter = self._check_filter(parsed[2:])
        self.session.set_session(
            action=parsed[0],
            model=model,
            filter=filter,
            user_cmd='_'.join(parsed[0:2])
        )

    def _want_all(self):
        return self.session.want_all

    def _set_for_all(self, parsed):
        if 'ALL' in parsed:
            parsed.remove('ALL')
            if 'VIEW' in parsed:
                self.session.set_session(want_all=True)
        return parsed

    def _check_filter(self, parsed):
        return '_'.join(parsed)
