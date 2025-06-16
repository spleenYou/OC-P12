import re
from datetime import date
from controllers.permissions import Permission
from functools import wraps


class Controller:
    def __init__(self, prompt, show, db, auth, session):
        self.session = session
        self.auth = auth(session)
        self.db = db(session, self.auth)
        self.show = show(self.db, session)
        self.prompt = prompt(self.show, self.db)
        self.allows_to = Permission(self.db, session)
        self.email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        self.phone_regex = re.compile(r'^\+?[0-9](?:\d{1,3} ?){1,5}\d{1,4}$')

    def check_token_and_perm(function):
        @wraps(function)
        def func_check(self, *args, **kwargs):
            if self.db.number_of_user() > 0:
                if not self.auth.check_token():
                    return False
            if not eval('self.allows_to.' + self.session.status.lower())():
                self.session.status = 'FORBIDDEN'
                return False
            return function(self, *args, **kwargs)
        return func_check

    def start(self, email):
        if self.db.number_of_user() == 0:
            self.show.wait()
            self.auth.generate_secret_key()
            self.session.new_user['department_id'] = 3
            self.session.user['department_id'] = 3
            self.session.new_user['email'] = email
            self.session.status = 'ADD_USER'
            if not self.add_user():
                self.show.wait()
                return None
            self.show.wait()
        self.session.status = 'CONNECTION'
        self.session.user["email"] = self.ask_email(email)
        password = self.prompt.thing('password')
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
            command = self.prompt.thing('command')
            command = command.upper().split(' ')
            if command[0] in ['HELP', 'EXIT', 'PERMISSION']:
                self.session.status = command[0]
            elif (command[0] in ['ADD', 'UPDATE', 'VIEW', 'DELETE'] and
                    command[1] in ['USER', 'CLIENT', 'CONTRACT', 'EVENT']):
                if (command[0] == 'ADD' or
                   (command[0] != 'ADD' and eval('self.db.number_of_' + command[1].lower())() > 0)):
                    if command[0] == 'UPDATE' and command[1] == 'EVENT' and self.session.user['department_id'] == 3:
                        command = command[0] + '_SUPPORT_ON_' + command[1]
                    else:
                        command = command[0] + '_' + command[1]
                    self.session.status = command
                    eval('self.' + command.replace('_SUPPORT_ON', '').lower())()
                else:
                    self.session.status = 'NO_' + command[1]
            else:
                self.session.status = 'UNKNOWN'
            if command != self.session.status or command[:4] == 'VIEW':
                self.show.wait()
            self.session.reset_session()

    def ask_name(self):
        name = self.prompt.thing('name')
        if name == '':
            name = self.session.new_user['name']
        return name

    def ask_email(self, email=None):
        status = self.session.status
        while email is None:
            self.session.status = status
            email = self.prompt.thing('email')
            if email == '':
                match status:
                    case 'UPDATE_USER':
                        email = self.session.new_user['email']
                    case 'UPDATE_CLIENT':
                        email = self.session.client['email']
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
            employee_number = self.prompt.thing('employee_number')
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
            password = self.prompt.thing('password')
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
        while department_id is None:
            self.session.status = status
            department_id = self.prompt.thing('department')
            if status == 'UPDATE_USER' and department_id == '':
                return self.session.new_user['department_id']
            try:
                department_id = int(department_id)
            except Exception:
                department_id = None
                self.session.status = 'BAD_DEPARTMENT'
                self.show.wait()
        return department_id

    def select_user(self):
        number = None
        status = self.session.status
        while number is None:
            self.session.status = 'SELECT_USER'
            number = self.prompt.thing('user')
            try:
                number = int(number)
                if number < self.db.number_of_user():
                    user_id = self.db.find_user_id(number)
                    self.session.status = status
                    return user_id
                else:
                    self.session.status = 'SELECT_USER_FAILED'
            except Exception:
                self.session.status = 'BAD_SELECT_USER'
            number = None
            self.show.wait()

    def ask_client_name(self):
        name = self.prompt.thing('client_name')
        if name == '':
            name = self.session.client['name']
        return name

    def ask_company_name(self):
        company_name = self.prompt.thing('company_name')
        if company_name == '':
            company_name = self.session.client['company_name']
        return company_name

    def ask_phone(self):
        phone = None
        status = self.session.status
        while phone is None:
            self.session.status = status
            phone = self.prompt.thing('phone')
            if status == 'UPDATE_CLIENT' and phone == '':
                phone = self.session.client['phone']
            if re.match(self.phone_regex, phone):
                return phone
            phone = None
            self.session.status = 'BAD_PHONE'
            self.show.wait()

    def ask_total_amount(self):
        total_amount = None
        status = self.session.status
        while total_amount is None:
            self.session.status = status
            total_amount = self.prompt.thing('total_amount')
            if status == 'UPDATE_CONTRACT' and total_amount == '':
                total_amount = self.session.contract['total_amount']
            try:
                total_amount = float(total_amount)
                return round(total_amount, 2)
            except Exception:
                total_amount = None
                self.session.status = 'BAD_TOTAL_AMOUNT'
                self.show.wait()

    def ask_rest_amount(self):
        rest_amount = None
        status = self.session.status
        while rest_amount is None:
            self.session.status = status
            rest_amount = self.prompt.thing('rest_amount')
            if status == 'UPDATE_CONTRACT' and rest_amount == '':
                rest_amount = self.session.contract['rest_amount']
            try:
                rest_amount = float(rest_amount)
                return round(rest_amount, 2)
            except Exception:
                rest_amount = None
                self.session.status = 'BAD_REST_AMOUNT'
                self.show.wait()

    def ask_status(self):
        contract_status = None
        status = self.session.status
        while contract_status is None:
            self.session.status = status
            contract_status = self.prompt.thing('contract_status').lower()
            if status == 'UPDATE_CONTRACT' and contract_status == '':
                contract_status = self.session.contract['status']
            if contract_status == 'y':
                return True
            elif contract_status == 'n':
                return False
            else:
                contract_status = None
                self.session.status = 'BAD_CONTRACT_STATUS'
                self.show.wait()

    @check_token_and_perm
    def add_user(self):
        self.session.new_user['name'] = self.ask_name()
        if self.session.new_user['email'] is None:
            self.session.new_user['email'] = self.ask_email()
        self.session.new_user['password'] = self.ask_password()
        self.session.new_user['employee_number'] = self.ask_employee_number()
        if self.session.new_user['department_id'] is None:
            self.session.new_user['department_id'] = self.ask_department()
        if self.prompt.validation():
            if self.db.add_user():
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
        self.session.new_user['password'] = self.auth.hash_password(self.ask_password())
        self.session.new_user['employee_number'] = self.ask_employee_number()
        self.session.new_user['department_id'] = self.ask_department()
        if self.prompt.validation():
            self.session.status = 'UPDATE_USER_OK'
            self.db.update_user()

    def view_user(self):
        user_id = self.select_user()
        self.session.new_user = self.db.get_user_information(user_id)

    @check_token_and_perm
    def delete_user(self):
        user_id = self.select_user()
        self.session.new_user = self.db.get_user_information(user_id)
        if self.prompt.validation():
            self.session.status = 'DELETE_USER_OK'
            self.db.delete_user(user_id)

    @check_token_and_perm
    def add_client(self):
        self.session.client['company_name'] = self.ask_company_name()
        self.session.client['name'] = self.ask_client_name()
        self.session.client['email'] = self.ask_email()
        self.session.client['phone'] = self.ask_phone()
        if self.prompt.validation():
            if self.db.add_client():
                self.session.status = 'ADD_CLIENT_OK'
            else:
                self.session.status = 'ADD_CLIENT_FAILED'

    @check_token_and_perm
    def update_client(self):
        client_id = self.select_client()
        self.session.client = self.db.get_client_information(client_id)
        self.session.new_user = self.db.get_user_information(self.session.client['commercial_contact_id'])
        self.session.client['company_name'] = self.ask_company_name()
        self.session.client['name'] = self.ask_client_name()
        self.session.client['email'] = self.ask_email()
        self.session.client['phone'] = self.ask_phone()
        if self.prompt.validation():
            if self.db.update_client():
                self.session.status = 'UPDATE_CLIENT_OK'
            else:
                self.session.status = 'UPDATE_CLIENT_FAILED'

    def view_client(self):
        client_id = self.select_client()
        self.session.client = self.db.get_client_information(client_id)
        self.session.new_user = self.db.get_user_information(self.session.client['commercial_contact_id'])

    @check_token_and_perm
    def delete_client(self):
        client_id = self.select_client()
        self.session.client = self.db.get_client_information(client_id)
        self.session.new_user = self.db.get_user_information(self.session.client['commercial_contact_id'])
        if self.prompt.validation():
            self.session.status = 'DELETE_CLIENT_OK'
            self.db.delete_client(client_id)
            self.db.delete_client(client_id)

    def select_client(self):
        status = self.session.status
        number = None
        while number is None:
            if status == 'ADD_EVENT':
                self.session.status = 'SELECT_CLIENT_WITHOUT_EVENT'
            elif status in ['UPDATE_EVENT', 'DELETE_EVENT', 'VIEW_EVENT']:
                self.session.status = 'SELECT_CLIENT_WITH_EVENT'
            else:
                self.session.status = 'SELECT_CLIENT'
            number = self.prompt.thing('client')
            try:
                number = int(number)
                if number < self.db.number_of_client():
                    self.session.status = status
                    return self.db.find_client_id(number)
                else:
                    self.session.status = 'SELECT_CLIENT_FAILED'
            except Exception:
                self.session.status = 'BAD_SELECT_CLIENT'
            number = None
            self.show.wait()

    @check_token_and_perm
    def add_contract(self):
        client_id = self.select_client()
        self.session.client = self.db.get_client_information(client_id)
        self.session.new_user = self.db.get_user_information(self.session.client['commercial_contact_id'])
        self.session.contract['total_amount'] = self.ask_total_amount()
        self.session.contract['rest_amount'] = self.ask_total_amount()
        if self.prompt.validation():
            if self.db.add_contract():
                self.session.status = 'ADD_CONTRACT_OK'
            else:
                self.session.status = 'ADD_CONTRACT_FAILED'

    @check_token_and_perm
    def update_contract(self):
        client_id = self.select_client()
        self.session.client = self.db.get_client_information(client_id)
        self.session.new_user = self.db.get_user_information(self.session.client['commercial_contact_id'])
        contract_id = self.select_contract()
        self.session.contract = self.db.get_contract_information(contract_id)
        self.session.contract['total_amount'] = self.ask_total_amount()
        self.session.contract['rest_amount'] = self.ask_rest_amount()
        self.session.contract['status'] = self.ask_status()
        print(type(self.session.status))
        if self.prompt.validation():
            if self.db.update_contract():
                self.session.status = 'UPDATE_CONTRACT_OK'
            else:
                self.session.status = 'UPDATE_CONTRACT_FAILED'

    @check_token_and_perm
    def delete_contract(self):
        client_id = self.select_client()
        self.session.client = self.db.get_client_information(client_id)
        self.session.new_user = self.db.get_user_information(self.session.client['commercial_contact_id'])
        contract_id = self.select_contract()
        self.session.contract = self.db.get_contract_information(contract_id)
        if self.prompt.validation():
            if self.db.update_contract():
                self.session.status = 'DELETE_CONTRACT_OK'
            else:
                self.session.status = 'DELETE_CONTRACT_FAILED'

    def view_contract(self):
        client_id = self.select_client()
        self.session.client = self.db.get_client_information(client_id)
        self.session.new_user = self.db.get_user_information(self.session.client['commercial_contact_id'])
        contract_id = self.select_contract()
        self.session.contract = self.db.get_contract_information(contract_id)

    def select_contract(self):
        status = self.session.status
        contract_id = None
        while contract_id is None:
            if status in ['ADD_EVENT']:
                self.session.status = 'SELECT_CONTRACT_WITHOUT_EVENT'
            elif status in ['UPDATE_EVENT', 'UPDATE_SUPPORT_ON_EVENT', 'DELETE_EVENT', 'VIEW_EVENT']:
                self.session.status = 'SELECT_CONTRACT_WITH_EVENT'
            else:
                self.session.status = 'SELECT_CONTRACT'
            contract_id = self.prompt.thing('contract')
            try:
                contract_id = int(contract_id)
                if contract_id < self.db.number_of_contract():
                    self.session.status = status
                    return self.db.find_contract_id(contract_id)
                else:
                    self.session.status = 'SELECT_CONTRACT_FAILED'
            except Exception:
                self.session.status = 'BAD_SELECT_CONTRACT'
            contract_id = None
            self.show.wait()

    @check_token_and_perm
    def add_event(self):
        nb_client = len(self.db.get_client_list())
        if self.db.number_of_support_user() > 0 and nb_client > 0:
            client_id = self.select_client()
            self.session.client = self.db.get_client_information(client_id)
            self.session.new_user = self.db.get_user_information(self.session.client['commercial_contact_id'])
            contract_id = self.select_contract()
            self.session.contract = self.db.get_contract_information(contract_id)
            self.session.event['location'] = self.ask_location()
            self.session.event['attendees'] = self.ask_attendees()
            self.session.event['date_start'] = self.ask_date_start()
            self.session.event['date_stop'] = self.ask_date_stop()
            self.session.event['notes'] = self.ask_notes()
            self.session.event['support_contact_id'] = self.select_support_user()
            if self.prompt.validation():
                if self.db.add_event():
                    self.session.status = 'ADD_EVENT_OK'
                else:
                    self.session.status = 'ADD_EVENT_FAILED'
        else:
            if nb_client == 0:
                self.session.status = 'NO_CLIENT_WITHOUT_EVENT'
            else:
                self.session.status = 'NO_SUPPORT_USER'

    @check_token_and_perm
    def update_event(self):
        client_id = self.select_client()
        self.session.client = self.db.get_client_information(client_id)
        self.session.new_user = self.db.get_user_information(self.session.client['commercial_contact_id'])
        contract_id = self.select_contract()
        self.session.contract = self.db.get_contract_information(contract_id)
        self.session.event = self.db.get_event_information()
        if self.session.status == 'UPDATE_EVENT':
            self.session.event['location'] = self.ask_location()
            self.session.event['attendees'] = self.ask_attendees()
            self.session.event['date_start'] = self.ask_date_start()
            self.session.event['date_stop'] = self.ask_date_stop()
            self.session.event['notes'] = self.ask_notes()
        self.session.event['support_contact_id'] = self.select_support_user()
        if self.prompt.validation():
            if self.db.update_event():
                self.session.status = 'UPDATE_EVENT_OK'
        else:
            self.session.status = 'UPDATE_EVENT_FAILED'

    @check_token_and_perm
    def delete_event(self):
        client_id = self.select_client()
        self.session.client = self.db.get_client_information(client_id)
        self.session.new_user = self.db.get_user_information(self.session.client['commercial_contact_id'])
        contract_id = self.select_contract()
        self.session.contract = self.db.get_contract_information(contract_id)
        self.session.event = self.db.get_event_information()
        if self.prompt.validation():
            if self.db.update_event():
                self.session.status = 'DELETE_EVENT_OK'
        else:
            self.session.status = 'DELETE_EVENT_FAILED'

    def view_event(self):
        client_id = self.select_client()
        self.session.client = self.db.get_client_information(client_id)
        self.session.new_user = self.db.get_user_information(self.session.client['commercial_contact_id'])
        contract_id = self.select_contract()
        self.session.contract = self.db.get_contract_information(contract_id)
        self.session.event = self.db.get_event_information()

    def ask_location(self):
        location = self.prompt.thing('location')
        if location == '':
            location = self.session.event['location']
        return location

    def ask_attendees(self):
        attendees = None
        status = self.session.status
        while attendees is None:
            self.session.status = status
            attendees = self.prompt.thing('attendees')
            if status == 'UPDATE_EVENT' and attendees == '':
                return self.session.event['attendees']
            try:
                attendees = int(attendees)
                return attendees
            except Exception:
                attendees = None
                self.session.status = 'BAD_ATTENDEES'
                self.show.wait()

    def ask_date_start(self):
        date_start = None
        status = self.session.status
        while date_start is None:
            self.session.status = status
            date_start = self.prompt.thing('date_start')
            if status == 'UPDATE_EVENT' and date_start == '':
                return self.session.event['date_start']
            try:
                day, month, year = date_start.split('/')
                date_start = date(year=int(year), month=int(month), day=int(day))
                return date_start
            except Exception:
                date_start = None
                self.session.status = 'BAD_DATE_START'
                self.show.wait()

    def ask_date_stop(self):
        date_stop = None
        status = self.session.status
        while date_stop is None:
            self.session.status = status
            date_stop = self.prompt.thing('date_stop')
            if status == 'UPDATE_EVENT' and date_stop == '':
                return self.session.event['date_stop']
            try:
                day, month, year = date_stop.split('/')
                date_stop = date(year=int(year), month=int(month), day=int(day))
                return date_stop
            except Exception:
                date_stop = None
                self.session.status = 'BAD_DATE_STOP'
                self.show.wait()

    def ask_notes(self):
        notes = self.prompt.thing('notes')
        if notes == '':
            notes = self.session.event['notes']
        return notes

    def select_support_user(self):
        user_id = None
        status = self.session.status
        while user_id is None:
            self.session.status = 'SELECT_SUPPORT_USER'
            user_id = self.prompt.thing('support_user')
            if status in ['UPDATE_EVENT', 'UPDATE_SUPPORT_ON_EVENT'] and user_id == '':
                self.session.status = status
                return self.session.event['support_contact_id']
            try:
                user_id = int(user_id)
                if user_id < self.db.number_of_user():
                    user_id = self.db.find_support_user_id(user_id)
                    self.session.status = status
                    return user_id
                else:
                    self.session.status = 'SELECT_SUPPORT_USER_FAILED'
            except Exception:
                self.session.status = 'BAD_SELECT_SUPPORT_USER'
            user_id = None
            self.show.wait()
