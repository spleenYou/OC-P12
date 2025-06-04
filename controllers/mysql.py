import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, EpicUser, Department, Permission, Client, Contract, Event
from argon2 import PasswordHasher
from controllers.authentication import Authentication
from sqlalchemy.exc import IntegrityError


class Mysql:
    def __init__(self):
        load_dotenv()
        self.engine = self.create_engine()
        Base.metadata.create_all(bind=self.engine)
        self.session = self.create_session()
        self.password_hasher = PasswordHasher(
            time_cost=int(os.getenv('TIME_COST')),
            memory_cost=int(os.getenv('MEMORY_COST')),
            parallelism=int(os.getenv('PARALLELISM')),
            hash_len=int(os.getenv('HASH_LEN')),
            salt_len=int(os.getenv('SALT_LEN'))
        )
        self.auth = Authentication()

    def create_engine(self):
        db_url = (f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
                  f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
        return create_engine(db_url)

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

    def has_epic_users(self):
        return self.session.query(EpicUser).count()

    def check_user_login(self, email, password):
        user_information = self.session.query(EpicUser) \
            .filter(EpicUser.email == email).first()
        if (user_information is not None and self.password_verification(password, user_information.password)):
            return user_information
        return None

    def get_department_list(self):
        return [d[0] for d in self.session.query(Department.name).order_by(Department.id).all()]

    def add_epic_user(self, name, email, password, employee_number, department_id):
        epic_user = EpicUser(
            name=name,
            email=email,
            password=self.hash_password(password),
            employee_number=employee_number,
            department_id=department_id
        )
        return self.add_in_db(epic_user)

    def update_epic_user(
            self,
            epic_user,
            name=None,
            email=None,
            password=None,
            employee_number=None,
            department_id=None):
        if name:
            epic_user.name = name
        if email:
            epic_user.email = email
        if password:
            epic_user.password = self.hash_password(password)
        if employee_number:
            epic_user.employee_number = employee_number
        if department_id:
            epic_user.department_id = department_id
        try:
            self.session.query(EpicUser).filter(EpicUser.id == epic_user.id).update(
                {
                    'name': epic_user.name,
                    'email': epic_user.email,
                    'password': epic_user.password,
                    'employee_number': epic_user.employee_number,
                    'department_id': epic_user.department_id
                }
            )
            self.session.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def get_epic_user_list(self):
        return self.session.query(EpicUser).all()

    def delete_epic_user(self, epic_user):
        try:
            self.session.delete(epic_user)
            self.session.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def add_client(self, name, email, phone, entreprise_name, commercial_contact_id):
        client = Client(
            name=name,
            email=email,
            phone=phone,
            entreprise_name=entreprise_name,
            commercial_contact_id=commercial_contact_id
        )
        return self.add_in_db(client)

    def update_client(
            self,
            client,
            name=None,
            email=None,
            phone=None,
            entreprise_name=None,
            commercial_contact_id=None):
        if name:
            client.name = name
        if email:
            client.email = email
        if phone:
            client.phone = phone
        if entreprise_name:
            client.entreprise_name = entreprise_name
        if commercial_contact_id:
            client.commercial_contact_id = commercial_contact_id
        try:
            self.session.query(Client).filter(Client.id == client.id).update(
                {
                    'name': client.name,
                    'email': client.email,
                    'phone': client.phone,
                    'entreprise_name': client.entreprise_name,
                    'commercial_contact_id': client.commercial_contact_id
                }
            )
            self.session.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def get_client_list(self):
        return self.session.query(Client).all()

    def delete_client(self, client):
        try:
            self.session.delete(client)
            self.session.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def add_contract(self, client_id, commercial_id, total_amount, rest_amount):
        contract = Contract(
            client_id=client_id,
            commercial_id=commercial_id,
            total_amount=total_amount,
            rest_amount=rest_amount
        )
        return self.add_in_db(contract)

    def update_contract(
            self,
            contract,
            client_id=None,
            commercial_id=None,
            total_amount=None,
            rest_amount=None,
            status=False):
        if client_id:
            contract.client_id = client_id
        if commercial_id:
            contract.commercial_id = commercial_id
        if total_amount:
            contract.total_amount = total_amount
        if rest_amount:
            contract.rest_amount = rest_amount
        if status:
            contract.status = status
        try:
            self.session.query(Contract).filter(Contract.id == contract.id).update(
                {
                    'client_id': contract.client_id,
                    'commercial_id': contract.commercial_id,
                    'total_amount': contract.total_amount,
                    'rest_amount': contract.rest_amount,
                    'status': contract.status
                }
            )
            self.session.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def get_contract_list(self, client):
        return self.session.query(Contract).filter(Contract.client_id == client.id).all()

    def delete_contract(self, contract):
        try:
            self.session.delete(contract)
            self.session.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def add_event(self, contract_id, client_id, support_contact_id, location, attendees, notes):
        event = Event(
            contract_id=contract_id,
            client_id=client_id,
            support_contact_id=support_contact_id,
            location=location,
            attendees=attendees,
            notes=notes
        )
        return self.add_in_db(event)

    def add_in_db(self, element_to_add):
        try:
            self.session.add(element_to_add)
            self.session.commit()
            return True
        except IntegrityError as e:
            print(f'IntegrityError : {e}')
            self.session.rollback()
            return False

    def get_permissions(self):
        return self.session.query(Permission).all()

    def hash_password(self, password):
        return self.password_hasher.hash(password)

    def password_verification(self, password, hash_password):
        try:
            return self.password_hasher.verify(hash_password, password)
        except Exception:
            return False
