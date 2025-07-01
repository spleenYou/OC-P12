import re
from datetime import date
from rich.prompt import Prompt, Confirm
from rich.console import Console
import config.prompts as prompts
import config.config as config


class NewPrompt(Prompt):
    prompt_suffix = ' '


class Ask:
    def __init__(self, show, db, session):
        self.display = show.display
        self.session = session
        self.db = db
        self.console = Console()
        self.email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        self.phone_regex = re.compile(r'^\+?[0-9](?:\d{1,3} ?){1,5}\d{1,4}$')

    def validation(self):
        """Shows a validation question

        Returns:
            bool: True by default
        """
        self.display()
        return Confirm.ask(
            f'\n[{config.validation_text_color}]{prompts.VALIDATION}[/{config.validation_text_color}]',
            default=True
        )

    def name(self):
        return self._pre_prompt('NAME', lambda: self.session.user.name)

    def notes(self):
        return self._pre_prompt('NOTES', lambda: self.session.contract.event.notes)

    def client_name(self):
        return self._pre_prompt('CLIENT_NAME', lambda: self.session.client.name)

    def company_name(self):
        return self._pre_prompt('COMPANY_NAME', lambda: self.session.client.company_name)

    def location(self):
        return self._pre_prompt('LOCATION', lambda: self.session.contract.event.location)

    def command(self):
        return self._pre_prompt('COMMAND')

    def date_start(self):
        return self._pre_prompt('DATE_START', lambda: self.session.contract.event.date_start)

    def date_stop(self):
        return self._pre_prompt('DATE_STOP', lambda: self.session.contract.event.date_start)

    def attendees(self):
        return self._pre_prompt('ATTENDEES', lambda: self.session.contract.event.attendees)

    def phone(self):
        return self._pre_prompt('PHONE', lambda: self.session.client.phone)

    def total_amount(self):
        return self._pre_prompt('TOTAL_AMOUNT', lambda: self.session.contract.total_amount)

    def rest_amount(self):
        self.session.set_session(filter='REST_AMOUNT')
        return self._pre_prompt('REST_AMOUNT', lambda: self.session.contract.rest_amount)

    def email(self):
        return self._pre_prompt('EMAIL', lambda: self.session.user.email)

    def client_email(self):
        return self._pre_prompt('CLIENT_EMAIL', lambda: self.session.client.email)

    def password(self):
        if self.session.filter == 'FIRST_TIME':
            self.session.connected_user.password = self._pre_prompt('PASSWORD')
            self.session.set_session(filter='SECOND_TIME')
            self.session.connected_user.password = self._pre_prompt('PASSWORD')
            self.session.set_session(action='CONNECTION', filter='')
            return None
        return self._pre_prompt('PASSWORD')

    def department(self):
        return self._pre_prompt('DEPARTMENT', lambda: self.session.user.department_id)

    def employee_number(self):
        return self._pre_prompt('EMPLOYEE_NUMBER', lambda: self.session.user.employee_number)

    def status(self):
        self.session.set_session(filter='STATUS')
        return self._pre_prompt('STATUS', lambda: self.session.contract.status)

    def wait(self):
        self._prompt('WAIT')

    def select(self, model):
        previous_filter = self.session.filter
        self.session.set_session(action='SELECT', model=model)
        self._set_filter(previous_filter)
        while True:
            self.session.set_session(state='NORMAL')
            number = self._prompt(model)
            if number == '' and self._no_change_allowed(model):
                self._restore_session(previous_filter)
                return None
            try:
                number = int(number)
                if self._is_number_valid(model, number):
                    self._set_session_model(model, number)
                    self._restore_session(previous_filter)
                    return None
                else:
                    self.session.set_session(state='ERROR')
            except Exception:
                self.session.set_session(state='FAILED')
            self.wait()

    def _restore_session(self, filter):
        parsed = self.session.user_cmd.split('_')
        self.session.set_session(filter=filter, action=parsed[0], model=parsed[1])

    def _is_number_valid(self, model, number):
        return number < self.db.number_of(model)

    def _no_change_allowed(self, model):
        return self.session.filter == 'SUPPORT'

    def _prompt(self, thing):
        self.display()
        if self.session.want_all and thing != 'WAIT':
            thing = thing + 'S'
        prompt = getattr(prompts, thing)
        is_password = False
        if thing == 'DEPARTMENT':
            departments = ' | '.join(f'{i + 1} {d}' for i, d in enumerate(self.db.get_department_list()))
            prompt = prompt.replace('departments', departments)
        if thing == 'PASSWORD':
            is_password = True
            if self.session.filter == 'SECOND_TIME':
                prompt = prompt[:-1] + '(vérification) :'
        return NewPrompt.ask(
            '\n[dark_orange3]  ' + prompt + '[/dark_orange3]',
            password=is_password,
            show_default=False
        )

    def _set_filter(self, previous_filter):
        if self.session.user_cmd in ['UPDATE_CONTRACT', 'DELETE_CONTRACT', 'VIEW_CONTRACT']:
            self.session.set_session(filter='WITH_CONTRACT')
        elif self.session.user_cmd == 'DELETE_USER':
            self.session.set_session(filter='FOR_DELETE')
        elif previous_filter != 'SUPPORT':
            if self.session.user_cmd == 'ADD_EVENT':
                self.session.set_session(filter='WITHOUT_EVENT')
            elif self.session.user_cmd in ['UPDATE_EVENT', 'DELETE_EVENT', 'VIEW_EVENT']:
                self.session.set_session(filter='WITH_EVENT')

    def _set_session_model(self, model, number):
        result = self.db.get(model, number)
        setattr(self.session, model.lower(), result)

    def _pre_prompt(self, thing, default_value=None):
        previous_user_cmd = self.session.user_cmd
        while True:
            self.session.set_session(user_cmd=previous_user_cmd, state='NORMAL')
            value = self._prompt(thing)
            if value == '':
                if self.session.action == 'ADD' and thing in config.is_nullable:
                    if thing == 'REST_AMOUNT':
                        return self.session.contract.total_amount
                    return None
                elif self.session.action == 'UPDATE':
                    return default_value()
                else:
                    self.session.set_session(user_cmd=thing.upper(), state='FAILED')
            else:
                success, value = self._is_accepted_value(thing, value)
                if success:
                    return value
                else:
                    self.session.set_session(user_cmd=thing.upper(), state="ERROR")
            self.wait()

    def _is_accepted_value(self, thing, value):
        list_method = {
            'is_text': self._is_text,
            'is_date': self._is_valid_date,
            'is_int': self._is_valid_int,
            'is_float': self._is_valid_float,
            'is_email': self._is_valid_email,
            'PHONE': self._is_valid_phone
        }
        for attr, method in list_method.items():
            if (hasattr(config, attr) and thing in getattr(config, attr)) or thing == attr:
                sucess, value = method(value)
                return sucess, value

    def _is_valid_phone(self, phone):
        return re.fullmatch(self.phone_regex, phone), phone

    def _is_valid_email(self, email):
        return re.fullmatch(self.email_regex, email), email

    def _is_text(self, value):
        if self.session.filter == 'SECOND_TIME':
            return value == self.session.connected_user.password, value
        if self.session.filter == 'STATUS':
            return True, True if value.lower() == 'y' else False
        return True, value

    def _is_valid_date(self, date_to_parse):
        success, value = self._try_convert(date_to_parse, self._parse_date)
        if not success:
            return False, None
        if self.session.event.date_start is None:
            success = value >= date.today()
        else:
            success = value >= self.session.event.date_start
        return success, value

    def _parse_date(self, date_to_parse):
        day, month, year = date_to_parse.split('/')
        return date(year=int(year), month=int(month), day=int(day))

    def _is_valid_float(self, number):
        success, value = self._try_convert(number, float)
        if value > (self.session.contract.total_amount or 0) and self.session.filter == 'REST_AMOUNT':
            value = self.session.contract.total_amount
        return success, value

    def _is_valid_int(self, number):
        success, value = self._try_convert(number, int)
        if success is True and self._is_employee_number():
            success = not self.db.employee_number_exits(value)
        if success is True and self._is_department():
            success = value > 0 and value < 4
        return success, value

    def _is_employee_number(self):
        return self.session.user_cmd == 'ADD_USER' and self.session.user.employee_number is None

    def _is_department(self):
        return self.session.user_cmd == 'ADD_USER' and self.session.user.employee_number is not None

    def _try_convert(self, value, func):
        try:
            value = func(value)
            return True, value
        except (ValueError, TypeError):
            return False, None
