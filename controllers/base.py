from controllers.permissions import Permission
from controllers.models import EpicUser
from functools import wraps
import constants as C


class Controller:
    def __init__(self, prompt, show, db, auth, session):
        self.session = session
        self.auth = auth(session)
        self.db = db(session, self.auth)
        self.client = None
        self.contract = None
        self.event = None
        self.show = show(session)
        self.prompt = prompt(self.show)
        self.allows_to = Permission(self.db, session)

    def check_token(function):
        @wraps(function)
        def func_check(self, *args, **kwargs):
            if not (self.session.status == C.FIRST_LAUNCH or
                    (self.auth.check_token() and eval('self.allows_to.' + function.__name__)())):
                return False
            return function(self, *args, **kwargs)
        return func_check

    def start(self):
        if self.db.has_epic_users() == 0:
            self.show.first_launch()
            self.show.wait()
            self.auth.generate_secret_key()
            self.session.user.department_id = 3
            self.add_user()
        self.session.status = C.CONNECTION
        if not self.session.user.email:
            self.session.user.email = self.prompt.for_email()
        password = self.prompt.for_password()
        self.user = self.auth.check_password(password, self.db.get_user_password())
        if self.user:
            self.session.first_launch = False
            self.auth.generate_token()
            self.show.logged_ok()
        else:
            self.show.logged_nok()

    @check_token
    def add_user(self):
        self.session.status = C.ADD_USER
        self.session.new_user = EpicUser()
        if self.session.first_launch:
            self.session.new_user = self.session.user
        self.session.new_user.name = self.prompt.for_name()
        if not self.session.new_user.email:
            self.session.new_user.email = self.prompt.for_email()
        self.session.new_user.password = self.prompt.for_password()
        self.session.new_user.employee_number = self.prompt.for_employee_number()
        if not self.session.new_user.department_id:
            self.session.new_user.department_id = self.prompt.for_department()
        if self.prompt.for_validation():
            self.db.add_epic_user()

    @check_token
    def add_client(self):
        if self.allows_to.add_client(self.user.department_id):
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
        return False

    def select_client(self):
        client_list = self.db.get_client_list()
        client = self.prompt.for_select_client(client_list)
        if client is not None:
            return client
        return None

    @check_token
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
