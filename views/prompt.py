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
        name = self._prompt('name')
        if name == '':
            name = self.session.new_user.name
        return name

    def notes(self):
        notes = self._prompt('notes')
        if self.session.status == 'UPDATE_EVENT' and notes == '':
            return self.session.contract.event.notes
        return notes

    def client_name(self):
        name = self._prompt('client_name')
        if name == '':
            name = self.session.client.name
        return name

    def company_name(self):
        company_name = self._prompt('company_name')
        if company_name == '':
            company_name = self.session.client.company_name
        return company_name

    def location(self):
        location = self._prompt('location')
        if location == '' and self.session.status == 'UPDATE_EVENT':
            return self.session.contract.event.location
        return location

    def date_start(self):
        date_start = None
        previous_status = self.session.status
        while date_start is None:
            self.session.state = 'NORMAL'
            self.session.status = previous_status
            date_start = self._prompt('date_start')
            if previous_status == 'UPDATE_EVENT' and date_start == '':
                return self.session.contract.event.date_start
            try:
                day, month, year = date_start.split('/')
                date_start = date(year=int(year), month=int(month), day=int(day))
                return date_start
            except Exception:
                date_start = None
                self.session.state = 'ERROR'
                self.session.status = 'DATE_START'
                self._prompt('wait')

    def date_stop(self):
        date_stop = None
        previous_status = self.session.status
        while date_stop is None:
            self.session.state = 'NORMAL'
            self.session.status = previous_status
            date_stop = self._prompt('date_stop')
            if previous_status == 'UPDATE_EVENT' and date_stop == '':
                return self.session.contract.event.date_stop
            try:
                day, month, year = date_stop.split('/')
                date_stop = date(year=int(year), month=int(month), day=int(day))
                return date_stop
            except Exception:
                date_stop = None
                self.session.state = 'ERROR'
                self.session.status = 'DATE_STOP'
                self._prompt('wait')

    def attendees(self):
        attendees = None
        previous_status = self.session.status
        while attendees is None:
            self.session.state = 'NORMAL'
            self.session.status = previous_status
            attendees = self._prompt('attendees')
            if previous_status == 'UPDATE_EVENT' and attendees == '':
                return self.session.contract.event.attendees
            try:
                attendees = int(attendees)
                return attendees
            except Exception:
                attendees = None
                self.session.state = 'ERROR'
                self.session.status = 'ATTENDEES'
                self._prompt('wait')

    def phone(self):
        phone = None
        previous_status = self.session.status
        while phone is None:
            self.session.state = 'NORMAL'
            self.session.status = previous_status
            phone = self._prompt('phone')
            if previous_status == 'UPDATE_CLIENT' and phone == '':
                phone = self.session.client.phone
            if re.match(self.phone_regex, phone):
                return phone
            phone = None
            self.session.state = 'ERROR'
            self.session.status = 'PHONE'
            self._prompt('wait')

    def total_amount(self):
        total_amount = None
        previous_status = self.session.status
        while total_amount is None:
            self.session.state = 'NORMAL'
            self.session.status = previous_status
            total_amount = self._prompt('total_amount')
            if previous_status == 'UPDATE_CONTRACT' and total_amount == '':
                total_amount = self.session.contract.total_amount
            try:
                total_amount = float(total_amount)
                return round(total_amount, 2)
            except Exception:
                total_amount = None
                self.session.state = 'ERROR'
                self.session.status = 'TOTAL_AMOUNT'
                self._prompt('wait')

    def rest_amount(self):
        rest_amount = None
        previous_status = self.session.status
        while rest_amount is None:
            self.session.state = 'NORMAL'
            self.session.status = previous_status
            rest_amount = self._prompt('rest_amount')
            if previous_status == 'UPDATE_CONTRACT' and rest_amount == '':
                rest_amount = self.session.contract.rest_amount
            try:
                rest_amount = float(rest_amount)
                return round(rest_amount, 2)
            except Exception:
                rest_amount = None
                self.session.state = 'ERROR'
                self.session.status = 'REST_AMOUNT'
                self._prompt('wait')

    def email(self, email=None):
        previous_status = self.session.status
        while email is None:
            self.session.status = previous_status
            self.session.state = 'NORMAL'
            email = self._prompt('email')
            if email == '':
                if previous_status == 'UPDATE_USER':
                    email = self.session.new_user.email
                elif previous_status == 'UPDATE_CLIENT':
                    email = self.session.client.email
            if not re.fullmatch(self.email_regex, email):
                self.session.status = 'EMAIL'
                self.session.state = 'FAILED'
                email = None
                self._prompt('wait')
        return email

    def password(self):
        previous_status = self.session.status
        password = None
        while password is None:
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
                    self.session.user.password = None
                    self._prompt('wait')
            else:
                self.session.status = 'PASSWORD'
                self.session.state = 'ERROR'
                self._prompt('wait')
            password = None

    def department(self):
        previous_status = self.session.status
        department_id = None
        if previous_status != 'UPDATE_USER':
            department_id = self.session.new_user.department_id
        while department_id is None:
            self.session.state = 'NORMAL'
            self.session.status = previous_status
            department_id = self._prompt('department')
            if previous_status == 'UPDATE_USER' and department_id == '':
                return self.session.new_user.department_id
            try:
                department_id = int(department_id)
            except Exception:
                self.session.state = 'ERROR'
                self.session.status = 'DEPARTMENT'
                department_id = None
                self._prompt('wait')
        return department_id

    def employee_number(self):
        previous_status = self.session.status
        employee_number = None
        while employee_number is None:
            self.session.status = previous_status
            self.session.state = 'NORMAL'
            employee_number = self._prompt('employee_number')
            if previous_status == 'UPDATE_USER' and employee_number == '':
                return self.session.new_user.employee_number
            try:
                employee_number = int(employee_number)
            except Exception:
                self.session.state = 'FAILED'
                self.session.status = 'EMPLOYEE_NUMBER'
                employee_number = None
                self._prompt('wait')
        return employee_number

    def status(self):
        contract_status = None
        previous_status = self.session.status
        while contract_status is None:
            self.session.state = 'NORMAL'
            self.session.status = previous_status
            contract_status = self._prompt('contract_status').lower()
            if previous_status == 'UPDATE_CONTRACT' and contract_status == '':
                return self.session.contract.status
            if contract_status == 'y':
                return True
            elif contract_status == 'n':
                return False
            else:
                contract_status = None
                self.session.state = 'ERROR'
                self.session.status = 'CONTRACT_STATUS'
                self._prompt('wait')

    def wait(self):
        self._prompt('wait')

    def command(self):
        return self._prompt('command')

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
