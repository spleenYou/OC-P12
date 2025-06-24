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
            f'\n[{config.validation_text_color}]{prompts.validation}[/{config.validation_text_color}]',
            default=True
        )

    def name(self):
        return self._pre_prompt('name', lambda: self.session.new_user.name)

    def notes(self):
        return self._pre_prompt(
            'notes',
            lambda: self.session.contract.event.notes,
            lambda: self.session.status == 'UPDATE_EVENT'
        )

    def client_name(self):
        return self._pre_prompt('client_name', lambda: self.session.client.name)

    def company_name(self):
        return self._pre_prompt('company_name', lambda: self.session.client.company_name)

    def location(self):
        return self._pre_prompt(
            'location',
            lambda: self.session.contract.event.location,
            lambda: self.session.status == 'UPDATE_EVENT'
        )

    def command(self):
        return self._pre_prompt('command')

    def date_start(self):
        return self._pre_prompt(
            'date_start',
            lambda: self.session.contract.event.date_start,
            lambda: self.session.status == 'UPDATE_EVENT',
        )

    def date_stop(self):
        return self._pre_prompt(
            'date_stop',
            lambda: self.session.contract.event.date_start,
            lambda: self.session.status == 'UPDATE_EVENT',
        )

    def attendees(self):
        return self._pre_prompt(
            'attendees',
            lambda: self.session.contract.event.attendees,
            lambda: self.session.status == 'UPDATE_EVENT',
        )

    def phone(self):
        return self._pre_prompt(
            'phone',
            lambda: self.session.client.phone,
            lambda: self.session.status == 'UPDATE_CLIENT'
        )

    def total_amount(self):
        return self._pre_prompt(
            'total_amount',
            lambda: self.session.contract.total_amount,
            lambda: self.session.status == 'UPDATE_CONTRACT',
        )

    def rest_amount(self):
        return self._pre_prompt(
            'rest_amount',
            lambda: self.session.contract.rest_amount,
            lambda: self.session.status == 'UPDATE_CONTRACT',
        )

    def email(self, email=None):
        return self._pre_prompt(
            'email',
            lambda: self.session.new_user.email,
            lambda: self.session.status == 'UPDATE_USER',
            email
        )

    def client_email(self):
        return self._pre_prompt(
            'client_email',
            lambda: self.session.client.email,
            lambda: self.session.status == 'UPDATE_CLIENT'
        )

    def password(self):
        previous_status = self.session.status
        while True:
            self.session.status = previous_status
            self.session.state = 'NORMAL'
            if self.session.filter == 'FIRST_TIME' and self.session.user.password is not None:
                self.session.filter = 'SECOND_TIME'
            password = self._prompt('password')
            if password != '':
                if self.session.status == 'CONNECTION':
                    return password
                elif self.session.user.password is None:
                    self.session.user.password = password
                elif password == self.session.user.password:
                    self.session.status = 'CONNECTION'
                    self.session.filter = ''
                    return None
                else:
                    self.session.status = 'PASSWORD'
                    self.session.state = 'FAILED'
                    self._prompt('wait')
            else:
                self.session.status = 'PASSWORD'
                self.session.state = 'ERROR'
                self._prompt('wait')

    def department(self):
        return self._pre_prompt(
            'department',
            lambda: self.session.new_user.department_id,
            lambda: self.session.status == 'UPDATE_USER'
        )

    def employee_number(self):
        return self._pre_prompt(
            'employee_number',
            lambda: self.session.new_user.employee_number,
            lambda: self.session.status == 'UPDATE_USER'
        )

    def status(self):
        self.session.filter == 'status'
        return self._pre_prompt(
            'status',
            lambda: self.session.contract.status,
            lambda: self.session.status == 'UPDATE_CONTRACT'
        )

    def wait(self):
        self._prompt('wait')

    def select(self, model):
        previous_filter = self.session.filter
        previous_status = self.session.status

        def restore_session():
            self.session.filter = previous_filter
            self.session.status = previous_status
        self.session.status = config.select_status[model]
        while True:
            self.session.state = 'NORMAL'
            self._set_filter(previous_status, previous_filter)
            number = self._prompt(model)
            if number == '' and self._no_change_allowed():
                restore_session()
                return None
            try:
                number = int(number)
                if self._is_number_valid(model, number):
                    self._set_session_model(model, number)
                    restore_session()
                    return None
                else:
                    self.session.state = 'FAILED'
            except Exception:
                self.session.state = 'ERROR'
            self.wait()

    def _is_number_valid(self, model, number):
        number_methods = {
            'user': self.db.number_of_user,
            'support': self.db.number_of_user,
            'client': self.db.number_of_client,
            'contract': self.db.number_of_contract,
        }
        return number < number_methods[model]()

    def _no_change_allowed(self):
        return self.session.filter == 'SUPPORT' and self.session.status == 'SELECT_USER'

    def _prompt(self, thing):
        self.display()
        prompt = getattr(prompts, thing)
        is_password = False
        if thing == 'department':
            departments = ' | '.join(f'{i + 1} {d}' for i, d in enumerate(self.db.get_department_list()))
            prompt = prompt.replace('departments', departments)
        if thing == 'password':
            is_password = True
            if self.session.filter == 'SECOND_TIME':
                prompt = prompt[:-1] + '(vérification) :'
        return NewPrompt.ask(
            '\n[dark_orange3]' + prompt + '[/dark_orange3]',
            password=is_password,
            show_default=False
        )

    def _set_filter(self, status, previous_filter):
        if status in ['UPDATE_CONTRACT', 'DELETE_CONTRACT', 'VIEW_CONTRACT']:
            self.session.filter = 'WITH_CONTRACT'
        elif status == 'DELETE_USER':
            self.session.filter = 'FOR_DELETE'
        elif previous_filter != 'SUPPORT':
            if status == 'ADD_EVENT':
                self.session.filter = 'WITHOUT_EVENT'
            elif status in ['UPDATE_EVENT', 'DELETE_EVENT', 'VIEW_EVENT']:
                self.session.filter = 'WITH_EVENT'

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

    def _pre_prompt(self, thing, default_value=None, condition=None, email=None):
        previous_status = self.session.status
        while True:
            self.session.state = 'NORMAL'
            if email:
                value = email
            else:
                value = self._prompt(thing)
            if value == '':
                if self.session.status.startswith('ADD') and thing in config.is_nullable:
                    return None
                elif condition is None or condition():
                    return default_value()
                else:
                    self.session.status = thing.upper()
                    self.session.state = 'FAILED'
            else:
                success, value = self._is_accepted_value(thing, value)
                if success:
                    return value
                else:
                    self.session.status = thing.upper()
                    self.session.state = "ERROR"
            self.wait()
            self.session.status = previous_status

    def _is_accepted_value(self, thing, value):
        list_method = {
            'is_text': self._is_text,
            'is_date': self._is_valid_date,
            'is_int': self._is_valid_int,
            'is_float': self._is_valid_float,
            'is_email': self._is_valid_email,
        }
        for attr, method in list_method.items():
            if thing in getattr(config, attr):
                sucess, value = method(value)
                return sucess, value

    def _is_valid_phone(self, phone):
        return re.fullmatch(self.phone_regex, phone), phone

    def _is_valid_email(self, email):
        return re.fullmatch(self.email_regex, email), email

    def _is_text(self, value):
        if self.session.filter == 'status':
            if value.lower() == 'y':
                return True, True
            return False, False
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
        return self._try_convert(number, float)

    def _is_valid_int(self, number):
        return self._try_convert(number, int)

    def _try_convert(self, value, func):
        try:
            value = func(value)
            return True, value
        except (ValueError, TypeError):
            return False, None
