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

    def has_users(self):
        return self.db_session.query(EpicUser).count()

    def get_user_information(self, email):
        user = self.db_session.query(EpicUser).filter(EpicUser.email == email).first()
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
            password=self.auth.hash_password(self.session.new_user['password']),
            employee_number=self.session.new_user['employee_number'],
            department_id=self.session.new_user['department_id']
        )
        return self.add_in_db(new_user)

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

    def get_user_password(self):
        password = self.db_session.query(EpicUser) \
            .with_entities(EpicUser.password) \
            .filter(EpicUser.email == self.session.user['email']).first()
        if password:
            return password[0]
        return False

    def get_user_list(self):
        return self.db_session.query(EpicUser).all()

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
            contract_id=self.session.user['id'],
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

    def get_event_information(self, event_id):
        event = self.db_session.query(Event).filter(Event.id == event_id).first()
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
