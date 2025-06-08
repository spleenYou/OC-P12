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

    def has_epic_users(self):
        return self.db_session.query(EpicUser).count()

    def get_epic_user_information(self, email):
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

    def add_epic_user(self):
        new_user = EpicUser()
        new_user.name = self.session.new_user['name']
        new_user.email = self.session.new_user['email']
        new_user.password = self.auth.hash_password(self.session.new_user['password'])
        new_user.employee_number = self.session.new_user['employee_number']
        new_user.department_id = self.session.new_user['department_id']
        return self.add_in_db(new_user)

    def update_epic_user(self):
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
        return self.db_session.query(EpicUser) \
            .with_entities(EpicUser.password) \
            .filter(EpicUser.email == self.session.user['email']).first()[0]

    def get_epic_user_list(self):
        return self.db_session.query(EpicUser).all()

    def delete_epic_user(self, epic_user):
        try:
            self.db_session.delete(epic_user)
            self.db_session.commit()
            return True
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def add_client(self):
        self.session.client.commercial_contact_id = self.session.user.id
        return self.add_in_db(self.session.client)

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
            self.db_session.query(Client).filter(Client.id == client.id).update(
                {
                    'name': client.name,
                    'email': client.email,
                    'phone': client.phone,
                    'entreprise_name': client.entreprise_name,
                    'commercial_contact_id': client.commercial_contact_id
                }
            )
            self.db_session.commit()
            return True
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def get_client_list(self):
        return self.db_session.query(Client).all()

    def delete_client(self, client):
        try:
            self.db_session.delete(client)
            self.db_session.commit()
            return True
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def add_contract(self, client_id, total_amount, rest_amount):
        contract = Contract(
            client_id=client_id,
            total_amount=total_amount,
            rest_amount=rest_amount
        )
        return self.add_in_db(contract)

    def update_contract(
            self,
            contract,
            client_id=None,
            total_amount=None,
            rest_amount=None,
            status=False):
        if client_id:
            contract.client_id = client_id
        if total_amount:
            contract.total_amount = total_amount
        if rest_amount:
            contract.rest_amount = rest_amount
        if status:
            contract.status = status
        try:
            self.db_session.query(Contract).filter(Contract.id == contract.id).update(
                {
                    'client_id': contract.client_id,
                    'total_amount': contract.total_amount,
                    'rest_amount': contract.rest_amount,
                    'status': contract.status
                }
            )
            self.db_session.commit()
            return True
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def get_contract_list(self, client):
        return self.db_session.query(Contract).filter(Contract.client_id == client.id).all()

    def delete_contract(self, contract):
        try:
            self.db_session.delete(contract)
            self.db_session.commit()
            return True
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def add_event(self, contract_id, support_contact_id, location, attendees, notes, date_start):
        event = Event(
            contract_id=contract_id,
            support_contact_id=support_contact_id,
            location=location,
            attendees=attendees,
            notes=notes,
            date_start=date_start
        )
        return self.add_in_db(event)

    def update_event(
            self,
            event,
            contract_id=None,
            support_contact_id=None,
            location=None,
            attendees=None,
            notes=None,
            date_start=None,
            date_stop=None):
        if contract_id:
            event.contract_id = contract_id
        if support_contact_id:
            event.support_contact_id = support_contact_id
        if location:
            event.location = location
        if attendees:
            event.attendees = attendees
        if notes:
            event.notes = notes
        if date_start:
            event.date_start = date_start
        if date_stop:
            event.date_stop = date_stop
        try:
            self.db_session.query(Event).filter(Event.id == event.id).update(
                {
                    'contract_id': event.contract_id,
                    'support_contact_id': event.support_contact_id,
                    'location': event.location,
                    'attendees': event.attendees,
                    'notes': event.notes,
                    'date_start': event.date_start,
                    'date_stop': event.date_stop
                }
            )
            self.db_session.commit()
            return True
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def get_event_list_by_client(self, client_id):
        return self.db_session.query(Event).join(Contract).filter(Contract.client_id == client_id).all()

    def get_event_list_by_epic_user(self, epic_user_id):
        return self.db_session.query(Event).join(EpicUser).filter(EpicUser.id == epic_user_id).all()

    def delete_event(self, event):
        try:
            self.db_session.delete(event)
            self.db_session.commit()
            return True
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
