import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, EpicUser, Department, Permission, Client, Contract, Event
from sqlalchemy.exc import IntegrityError


class Mysql:
    def __init__(self, session, authentication):
        load_dotenv()
        self.engine = self.create_engine()
        Base.metadata.create_all(bind=self.engine)
        self.db_session = self.create_session()
        self.session = session
        self.auth = authentication

    def create_engine(self):
        db_url = (f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
                  f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
        return create_engine(db_url)

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

    def number_of_user(self):
        if self.session.status == 'SELECT_USER_FOR_DELETE':
            return self.db_session.query(EpicUser).filter(EpicUser.id == self.session.user['id']).count()
        return self.db_session.query(EpicUser).count()

    def number_of_support_user(self):
        return self.db_session.query(EpicUser).filter(EpicUser.department_id == 2).count()

    def number_of_client(self):
        if self.session.status == 'SELECT_CLIENT_WITH_CONTRACT':
            return self.db_session.query(Client).filter(Client.contracts.any()).count()
        return self.db_session.query(Client).count()

    def number_of_contract(self):
        if self.session.client['id'] is None:
            return self.db_session.query(Contract).count()
        elif self.session.status == 'SELECT_CONTRACT_WITHOUT_EVENT':
            return self.db_session.query(Contract) \
                    .filter((Contract.client_id == self.session.client['id']) & ~Contract.event.any()) \
                    .count()
        elif self.session.status == 'SELECT_CONTRACT_WITH_EVENT':
            return self.db_session.query(Contract) \
                    .filter((Contract.client_id == self.session.client['id']) & Contract.event.any()) \
                    .count()
        return self.db_session.query(Contract).filter(Contract.client_id == self.session.client['id']).count()

    def number_of_event(self):
        return self.db_session.query(Event).count()

    def get_user_information(self, user_id):
        user = self.db_session.query(EpicUser).filter(EpicUser.id == user_id).first()
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'password': user.password,
            'employee_number': user.employee_number,
            'department_id': user.department_id
        }

    def get_department_list(self):
        return [d[0] for d in self.db_session.query(Department.name).order_by(Department.id).all()]

    def add_user(self):
        new_user = EpicUser(
            name=self.session.new_user['name'],
            email=self.session.new_user['email'],
            password=None,
            employee_number=self.session.new_user['employee_number'],
            department_id=self.session.new_user['department_id']
        )
        return self.add_in_db(new_user)

    def update_password_user(self):
        count = self.db_session.query(EpicUser) \
            .filter(EpicUser.email == self.session.user['email']) \
            .update({'password': self.auth.hash_password(self.session.user['password'])})
        self.db_session.commit()
        return count > 0

    def update_user(self):
        print(self.session.new_user)
        try:
            count = self.db_session.query(EpicUser).filter(EpicUser.id == self.session.new_user['id']).update(
                {
                    'name': self.session.new_user['name'],
                    'email': self.session.new_user['email'],
                    'password': self.session.new_user['password'],
                    'employee_number': self.session.new_user['employee_number'],
                    'department_id': self.session.new_user['department_id']
                }
            )
            self.db_session.commit()
            return count > 0
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def get_user_id(self, email):
        return self.db_session.query(EpicUser.id).filter(EpicUser.email == email).first()[0]

    def find_user_id(self, number):
        if self.session.status == 'SELECT_USER_FOR_DELETE':
            return self.db_session \
                    .query(EpicUser.id) \
                    .filter(EpicUser.id != self.session.user['id']) \
                    .order_by(EpicUser.id) \
                    .all()[number][0]
        return self.db_session.query(EpicUser.id).order_by(EpicUser.id).all()[number][0]

    def find_support_user_id(self, number):
        return self.db_session.query(EpicUser.id) \
            .filter(EpicUser.department_id == 2) \
            .order_by(EpicUser.id) \
            .all()[number][0]

    def find_client_id(self, number):
        if self.session.status == 'SELECT_CLIENT_WITH_CONTRACT':
            return self.db_session.query(Client.id) \
                        .filter(Client.contracts.any()) \
                        .order_by(Client.id) \
                        .all()[number][0]
        if self.session.status == 'SELECT_CLIENT_WITHOUT_EVENT':
            return self.db_session.query(Client.id) \
                        .filter((Client.contracts.any()) & (~Client.contracts.any(Contract.event.any()))) \
                        .order_by(Client.id) \
                        .all()[number][0]
        if self.session.status == 'SELECT_CLIENT_WITH_EVENT':
            return self.db_session.query(Client.id) \
                        .filter(Client.contracts.any(Contract.event.any())) \
                        .order_by(Client.id) \
                        .all()[number][0]
        else:
            return self.db_session.query(Client.id).order_by(Client.id).all()[number][0]

    def find_contract_id(self, number):
        if self.session.status == 'SELECT_CONTRACT_WITHOUT_EVENT':
            return self.db_session.query(Contract.id) \
                    .filter((Contract.client_id == self.session.client['id']) & ~Contract.event.any()) \
                    .order_by(Contract.id) \
                    .all()[number][0]
        if self.session.status == 'SELECT_CONTRACT_WITH_EVENT':
            return self.db_session.query(Contract.id) \
                    .filter((Contract.client_id == self.session.client['id']) & Contract.event.any()) \
                    .order_by(Contract.id) \
                    .all()[number][0]
        return self.db_session.query(Contract.id) \
            .filter(Contract.client_id == self.session.client['id']) \
            .order_by(Contract.id) \
            .all()[number][0]

    def get_user_password(self):
        password = self.db_session.query(EpicUser) \
            .with_entities(EpicUser.password) \
            .filter(EpicUser.email == self.session.user['email']).first()
        if password:
            return password[0]
        return False

    def get_user_list(self):
        if self.session.status == 'SELECT_USER_FOR_DELETE':
            return self.db_session \
                    .query(EpicUser) \
                    .filter(EpicUser.id != self.session.user['id']) \
                    .order_by(EpicUser.id).all()
        return self.db_session.query(EpicUser).order_by(EpicUser.id).all()

    def get_support_user_list(self):
        return self.db_session.query(EpicUser).filter(EpicUser.department_id == 2).order_by(EpicUser.id).all()

    def delete_user(self, user_id):
        try:
            count = self.db_session.query(EpicUser).filter(EpicUser.id == user_id).delete()
            self.db_session.commit()
            return count > 0
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def add_client(self):
        new_client = Client(
            name=self.session.client['name'],
            email=self.session.client['email'],
            phone=self.session.client['phone'],
            company_name=self.session.client['company_name'],
            commercial_contact_id=self.session.user['id']
        )
        return self.add_in_db(new_client)

    def update_client(self):
        try:
            count = self.db_session.query(Client).filter(Client.id == self.session.client['id']).update(
                {
                    'name': self.session.client['name'],
                    'email': self.session.client['email'],
                    'phone': self.session.client['phone'],
                    'company_name': self.session.client['company_name'],
                    'commercial_contact_id': self.session.client['commercial_contact_id']
                }
            )
            self.db_session.commit()
            return count > 0
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def get_client_list(self):
        if self.session.status == 'SELECT_CLIENT_WITH_EVENT':
            return self.db_session.query(Client).filter(Client.contracts.any(Contract.event.any())).all()
        elif self.session.status in ['SELECT_CLIENT_WITHOUT_EVENT', 'ADD_EVENT']:
            return self.db_session.query(Client) \
                        .filter((Client.contracts.any()) & (Client.contracts.any(~Contract.event.any()))) \
                        .all()
        elif self.session.status == 'SELECT_CLIENT_WITH_CONTRACT':
            return self.db_session.query(Client) \
                        .filter(Client.contracts.any()) \
                        .all()
        else:
            return self.db_session.query(Client).all()

    def get_client_information(self, client_id):
        client = self.db_session.query(Client).filter(Client.id == client_id).first()
        return {
            'id': client.id,
            'name': client.name,
            'email': client.email,
            'phone': client.phone,
            'company_name': client.company_name,
            'commercial_contact_id': client.commercial_contact_id
        }

    def delete_client(self, client_id):
        try:
            count = self.db_session.query(Client).filter(Client.id == client_id).delete()
            self.db_session.commit()
            return count > 0
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def add_contract(self):
        contract = Contract(
            client_id=self.session.client['id'],
            total_amount=self.session.contract['total_amount'],
            rest_amount=self.session.contract['total_amount']
        )
        return self.add_in_db(contract)

    def update_contract(self):
        try:
            count = self.db_session.query(Contract).filter(Contract.id == self.session.contract['id']).update(
                {
                    'client_id': self.session.client['id'],
                    'total_amount': self.session.contract['total_amount'],
                    'rest_amount': self.session.contract['rest_amount'],
                    'status': self.session.contract['status']
                }
            )
            self.db_session.commit()
            return count > 0
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def get_contract_list(self):
        if self.session.status == 'SELECT_CONTRACT_WITH_EVENT':
            return self.db_session.query(Contract) \
                    .filter(Contract.client_id == self.session.client['id']) \
                    .join(Event) \
                    .filter(Event.contract_id == Contract.id) \
                    .all()
        elif self.session.status == 'SELECT_CONTRACT_WITHOUT_EVENT':
            return self.db_session.query(Contract) \
                    .filter((Contract.client_id == self.session.client['id']) & ~Contract.event.any()) \
                    .all()
        else:
            return self.db_session.query(Contract).filter(Contract.client_id == self.session.client['id']).all()

    def get_contract_information(self, contract_id):
        contract = self.db_session.query(Contract).filter(Contract.id == contract_id).first()
        return {
            'id': contract.id,
            'total_amount': contract.total_amount,
            'rest_amount': contract.rest_amount,
            'status': contract.status,
        }

    def delete_contract(self, contract_id):
        try:
            count = self.db_session.query(Contract).filter(Contract.id == contract_id).delete()
            self.db_session.commit()
            return count > 0
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def add_event(self):
        event = Event(
            contract_id=self.session.contract['id'],
            support_contact_id=self.session.event['support_contact_id'],
            location=self.session.event['location'],
            attendees=self.session.event['attendees'],
            notes=self.session.event['notes'],
            date_start=self.session.event['date_start'],
            date_stop=self.session.event['date_stop']
        )
        return self.add_in_db(event)

    def update_event(self):
        try:
            count = self.db_session.query(Event).filter(Event.id == self.session.event['id']).update(
                {
                    'contract_id': self.session.event['contract_id'],
                    'support_contact_id': self.session.event['support_contact_id'],
                    'location': self.session.event['location'],
                    'attendees': self.session.event['attendees'],
                    'notes': self.session.event['notes'],
                    'date_start': self.session.event['date_start'],
                    'date_stop': self.session.event['date_stop']
                }
            )
            self.db_session.commit()
            return count > 0
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def get_event_list_by_client(self, client_id):
        return self.db_session.query(Event).join(Contract).filter(Contract.client_id == client_id).all()

    def get_event_list_by_user(self, user_id):
        events = self.db_session.query(Event).join(EpicUser).filter(EpicUser.id == user_id).all()
        if not events:
            events = self.db_session.query(Event) \
                .join(Contract).filter(Event.contract_id == Contract.id) \
                .join(Client).filter(Contract.client_id == Client.id) \
                .all()
        return events

    def get_event_information(self):
        print(self.session.contract['id'])
        print(self.db_session.query(Event).first().contract_id)
        event = self.db_session.query(Event).filter(Event.contract_id == self.session.contract['id']).first()
        return {
            'id': event.id,
            'support_contact_id': event.support_contact_id,
            'location': event.location,
            'attendees': event.attendees,
            'notes': event.notes,
            'date_start': event.date_start,
            'date_stop': event.date_stop,
            'contract_id': event.contract_id
        }

    def delete_event(self):
        try:
            count = self.db_session.query(Event).filter(Event.id == self.session.event['id']).delete()
            self.db_session.commit()
            return count > 0
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def add_in_db(self, element_to_add):
        try:
            self.db_session.add(element_to_add)
            self.db_session.commit()
            return True
        except IntegrityError as e:
            print(f'IntegrityError : {e}')
            self.db_session.rollback()
            return False

    def get_permissions(self):
        return self.db_session.query(Permission).all()
