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
        if self.session.filter == 'FOR_DELETE':
            return self.db_session.query(EpicUser).filter(EpicUser != self.session.user).count()
        return self.db_session.query(EpicUser).count()

    def number_of_support_user(self):
        return self.db_session.query(EpicUser).filter(EpicUser.department_id == 2).count()

    def number_of_client(self):
        if self.session.filter == 'WITH_CONTRACT':
            return self.db_session.query(Client).filter(Client.contracts.any()).count()
        return self.db_session.query(Client).count()

    def number_of_contract(self):
        if self.session.client.id is None:
            return self.db_session.query(Contract).count()
        elif self.session.filter == 'WITHOUT_EVENT':
            return self.db_session.query(Contract) \
                .filter((Contract.client_id == self.session.client.id)) \
                .filter(~Contract.event.has()) \
                .count()
        elif self.session.filter == 'WITH_EVENT':
            return self.db_session.query(Contract) \
                .filter((Contract.client_id == self.session.client.id)) \
                .filter(Contract.event.has()) \
                .count()
        return self.db_session.query(Contract).filter(Contract.client_id == self.session.client.id).count()

    def number_of_event(self):
        return self.db_session.query(Event).count()

    def get_department_list(self):
        return [d[0] for d in self.db_session.query(Department.name).order_by(Department.id).all()]

    def add_user(self):
        return self.add_in_db(self.session.new_user)

    def update_password_user(self):
        count = self.db_session.query(EpicUser) \
            .filter(EpicUser.email == self.session.user.email) \
            .update({'password': self.auth.hash_password(self.session.user.password)})
        self.db_session.commit()
        return count > 0

    def get_user_by_mail(self, email):
        return self.db_session.query(EpicUser).filter(EpicUser.email == email).first()
        return self.db_session.query(EpicUser).filter(EpicUser.email == email).first()

    def get_user_by_number(self, number):
        if self.session.filter == 'FOR_DELETE':
            return self.db_session \
                    .query(EpicUser) \
                    .filter(EpicUser != self.session.user) \
                    .order_by(EpicUser.id) \
                    .all()[number]
        return self.db_session.query(EpicUser).order_by(EpicUser.id).all()[number]

    def get_support_user_by_id(self, number):
        return self.db_session.query(EpicUser.id) \
            .filter(EpicUser.department_id == 2) \
            .order_by(EpicUser.id) \
            .all()[number][0]

    def get_client(self, number):
        if self.session.filter == 'WITH_CONTRACT':
            return self.db_session.query(Client) \
                        .filter(Client.contracts.any()) \
                        .order_by(Client.id) \
                        .all()[number]
        if self.session.filter == 'WITHOUT_EVENT':
            return self.db_session.query(Client) \
                        .filter(Client.contracts.any(~Contract.event.has())) \
                        .order_by(Client.id) \
                        .all()[number]
        if self.session.filter == 'WITH_EVENT':
            return self.db_session.query(Client) \
                        .filter(Client.contracts.any(Contract.event.has())) \
                        .order_by(Client.id) \
                        .all()[number]
        else:
            return self.db_session.query(Client).order_by(Client.id).all()[number]

    def get_contract(self, number):
        if self.session.filter == 'WITHOUT_EVENT':
            return self.db_session.query(Contract) \
                    .filter(Contract.client_id == self.session.client.id) \
                    .filter(~Contract.event.has()) \
                    .order_by(Contract.id) \
                    .all()[number]
        if self.session.filter == 'WITH_EVENT':
            return self.db_session.query(Contract) \
                    .filter(Contract.client_id == self.session.client.id) \
                    .filter(Contract.event.has()) \
                    .order_by(Contract.id) \
                    .all()[number]
        return self.db_session.query(Contract) \
            .filter(Contract.client_id == self.session.client.id) \
            .order_by(Contract.id) \
            .all()[number]

    def get_user_password(self):
        password = self.db_session.query(EpicUser) \
            .with_entities(EpicUser.password) \
            .filter(EpicUser.email == self.session.user.email).first()
        if password:
            return password[0]
        return False

    def get_user_list(self):
        if self.session.filter == 'FOR_DELETE':
            return self.db_session \
                    .query(EpicUser) \
                    .filter(EpicUser.id != self.session.user.id) \
                    .order_by(EpicUser.id).all()
        return self.db_session.query(EpicUser).order_by(EpicUser.id).all()

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
        return self.add_in_db(self.session.client)

    def get_client_list(self):
        if self.session.filter == 'WITH_EVENT':
            return self.db_session.query(Client).filter(Client.contracts.any(Contract.event.has())).all()
        elif self.session.filter == 'WITHOUT_EVENT':
            return self.db_session.query(Client) \
                        .filter(~Client.contracts.any(Contract.event.has())) \
                        .all()
        elif self.session.filter == 'WITH_CONTRACT':
            return self.db_session.query(Client) \
                        .filter(Client.contracts.any()) \
                        .all()
        else:
            return self.db_session.query(Client).all()

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
        return self.add_in_db(self.session.contract)

    def get_contract_list(self):
        if self.session.filter == 'WITH_EVENT':
            return self.db_session.query(Contract) \
                    .filter((Contract.client_id == self.session.client.id)) \
                    .filter(Contract.event.has()) \
                    .all()
        elif self.session.filter == 'WITHOUT_EVENT':
            return self.db_session.query(Contract) \
                    .filter(Contract.client_id == self.session.client.id) \
                    .filter(~Contract.event.has()) \
                    .all()
        else:
            return self.db_session.query(Contract).filter(Contract.client_id == self.session.client.id).all()

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
        return self.add_in_db(self.session.event)

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
