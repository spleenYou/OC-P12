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
        query = self.db_session.query(EpicUser)
        filters = {
            'FOR_DELETE': lambda q: q.filter(EpicUser != self.session.user),
        }
        if self.session.filter in filters:
            query = filters[self.session.filter](query)
        return query.count()

    def number_of_support_user(self):
        return self.db_session.query(EpicUser).filter(EpicUser.department_id == 2).count()

    def number_of_client(self):
        query = self.db_session.query(Client)
        filters = {
            'WITH_CONTRACT': lambda q: q.filter(Client.contracts.any()),
        }
        if self.session.filter in filters:
            query = filters[self.session.filter](query)
        return query.count()

    def number_of_contract(self):
        if self.session.client.id is None:
            return self.db_session.query(Contract).count()
        query = self.db_session.query(Contract).filter(Contract.client_id == self.session.client.id)
        filters = {
            'WITH_EVENT': lambda q: q.filter(Contract.event.has()),
            'WITHOUT_EVENT': lambda q: q.filter(~Contract.event.has()),
        }
        if self.session.filter in filters:
            query = filters[self.session.filter](query)
        return query.count()

    def number_of_event(self):
        return self.db_session.query(Event).count()

    def get_department_list(self):
        return [d[0] for d in self.db_session.query(Department.name).order_by(Department.id).all()]

    def add_user(self):
        return self._add_in_db(self.session.new_user)

    def update_password_user(self):
        count = self.db_session.query(EpicUser) \
            .filter(EpicUser.email == self.session.user.email) \
            .update({'password': self.auth.hash_password(self.session.user.password)})
        self.db_session.commit()
        return count > 0

    def get_user_by_mail(self, email):
        return self.db_session.query(EpicUser).filter(EpicUser.email == email).first()

    def get_user_by_number(self, number):
        query = self.db_session.query(EpicUser).order_by(EpicUser.id)
        filters = {
            'SUPPORT': lambda q: q.filter(EpicUser.department_id == 2),
            'FOR_DELETE': lambda q: q.filter(EpicUser != self.session.user),
        }
        if self.session.filter in filters:
            query = filters[self.session.filter](query)
        return query.all()[number]

    def get_user_by_id(self, id):
        return self.db_session.query(EpicUser) \
            .filter(EpicUser.id == id) \
            .first()

    def get_client(self, number):
        query = self.db_session.query(Client).order_by(Client.id)
        filters = {
            'WITH_EVENT': lambda q: q.filter(Client.contracts.any(Contract.event.has())),
            'WITHOUT_EVENT': lambda q: q.filter(Client.contracts.any(~Contract.event.has())),
            'WITH_CONTRACT': lambda q: q.filter(Client.contracts.any()),
        }
        if self.session.filter in filters:
            query = filters[self.session.filter](query)
        return query.all()[number]

    def get_contract(self, number):
        query = self.db_session.query(Contract) \
                    .filter(Contract.client_id == self.session.client.id) \
                    .order_by(Contract.id)
        filters = {
            'WITH_EVENT': lambda q: q.filter(Contract.event.has()),
            'WITHOUT_EVENT': lambda q: q.filter(~Contract.event.has()),
        }
        if self.session.filter in filters:
            query = filters[self.session.filter](query)
        return query.all()[number]

    def get_user_password(self):
        password = self.db_session.query(EpicUser) \
            .with_entities(EpicUser.password) \
            .filter(EpicUser.email == self.session.user.email).first()
        if password:
            return password[0]
        return None

    def get_user_list(self):
        query = self.db_session.query(EpicUser).order_by(EpicUser.id)
        filters = {
            'FOR_DELETE': lambda q: q.filter(EpicUser.id != self.session.user.id),
        }
        if self.session.filter in filters:
            query = filters[self.session.filter](query)
        return query.all()

    def get_support_user_list(self):
        return self.db_session.query(EpicUser).filter(EpicUser.department_id == 2).order_by(EpicUser.id).all()

    def delete_user(self):
        try:
            self.db_session.delete(self.session.new_user)
            result = self.session.new_user in self.db_session.deleted
            self.db_session.commit()
            return result
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def add_client(self):
        self.session.client.commercial_contact_id = self.session.user.id
        return self._add_in_db(self.session.client)

    def get_client_list(self):
        query = self.db_session.query(Client)
        filters = {
            'WITH_EVENT': lambda q: q.filter(Client.contracts.any(Contract.event.has())),
            'WITHOUT_EVENT': lambda q: q.filter(~Client.contracts.any(Contract.event.has())),
            'WITH_CONTRACT': lambda q: q.filter(Client.contracts.any()),
        }
        if self.session.filter in filters:
            query = filters[self.session.filter](query)
        return query.all()

    def delete_client(self):
        try:
            self.db_session.delete(self.session.client)
            result = self.session.client in self.db_session.deleted
            self.db_session.commit()
            return result
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def add_contract(self):
        self.session.contract.client_id = self.session.client.id
        return self._add_in_db(self.session.contract)

    def get_contract_list(self):
        query = self.db_session.query(Contract).filter(Contract.client_id == self.session.client.id)
        filters = {
            'WITH_EVENT': lambda q: q.filter(Contract.event.has()),
            'WITHOUT_EVENT': lambda q: q.filter(~Contract.event.has()),
        }
        if self.session.filter in filters:
            query = filters[self.session.filter](query)
        return query.all()

    def delete_contract(self):
        try:
            self.db_session.delete(self.session.contract)
            result = self.session.contract in self.db_session.deleted
            self.db_session.commit()
            return result
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def add_event(self):
        self.session.event.contract_id = self.session.contract.id
        return self._add_in_db(self.session.event)

    def delete_event(self):
        try:
            self.db_session.delete(self.session.contract.event)
            result = self.session.contract.event in self.db_session.deleted
            self.db_session.commit()
            return result
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def _add_in_db(self, element_to_add):
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

    def get_event_list(self):
        query = self.db_session.query(Event)
        filters = {
            'WITHOUT_SUPPORT': lambda q: q.filter(~Event.support_contact.has()),
        }
        if self.session.filter in filters:
            query = filters[self.session.filter](query)
        return query.all()
