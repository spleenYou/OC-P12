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

    def number_of(self, model):
        self.db_session.rollback()
        query = self.db_session.query(self._get_model(model))
        query = self._get_filter_method(model)(query)
        return query.count()

    def get(self, model, number):
        self.db_session.rollback()
        query = self.db_session.query(self._get_model(model))
        query = self._get_filter_method(model)(query)
        return query.all()[number]

    def get_list(self, model):
        self.db_session.rollback()
        query = self.db_session.query(self._get_model(model))
        query = self._get_filter_method(model)(query)
        return query.all()

    def get_department_list(self):
        return [d[0] for d in self.db_session.query(Department.name).order_by(Department.id).all()]

    def update_password_user(self, email):
        count = self.db_session.query(EpicUser) \
                    .filter(EpicUser.email == email) \
                    .update({'password': self.auth.hash_password(self.session.connected_user.password)})
        self.db_session.commit()
        return count > 0

    def get_user_password(self, email):
        self.db_session.rollback()
        password = self.db_session.query(EpicUser) \
            .with_entities(EpicUser.password) \
            .filter(EpicUser.email == email).first()
        if password:
            return password[0]
        return None

    def delete(self):
        self.db_session.rollback()
        try:
            attr = getattr(self.session, self.session.model.lower())
            self.db_session.delete(attr)
            result = attr in self.db_session.deleted
            self.db_session.commit()
            return result
        except Exception:
            self.db_session.rollback()
            return False

    def get_permissions(self):
        return self.db_session.query(Permission).all()

    def employee_number_exits(self, employee_number):
        self.db_session.rollback()
        return self.db_session.query(EpicUser).filter(EpicUser.employee_number == employee_number).first()

    def add(self):
        self.db_session.rollback()
        try:
            self._fill_missing_field(self.session.model)
            self.db_session.add(getattr(self.session, self.session.model.lower()))
            self.db_session.commit()
            return True
        except IntegrityError:
            self.db_session.rollback()
            return False

    def _user_filter(self, query):
        filters = {
            'FOR_DELETE': lambda q: q.filter(EpicUser.id != self.session.connected_user.id),
            'COMMERCIAL': lambda q: q.filter(EpicUser.department_id == 1),
            'SUPPORT': lambda q: q.filter(EpicUser.department_id == 2),
            'MANAGEMENT': lambda q: q.filter(EpicUser.department_id == 3),
            'EMAIL': lambda q: q.filter(EpicUser.email == self.session.connected_user.email),
            'ID': lambda q: q.filter(EpicUser.id == self.session.user.id),
        }
        return self._apply_filter(query, filters)

    def _client_filter(self, query):
        filters = {
            'WITH_EVENT': lambda q: q.filter(Client.contracts.any(Contract.event.has())),
            'WITHOUT_EVENT': lambda q: q.filter(Client.contracts.any(~Contract.event.has())),
            'WITH_CONTRACT': lambda q: q.filter(Client.contracts.any()),
            'WITHOUT_CONTRACT': lambda q: q.filter(~Client.contracts.any()),
        }
        if not self._for_all() and self.session.connected_user.department_id == 1:
            query = query.filter(Client.commercial_contact_id == self.session.connected_user.id)
        return self._apply_filter(query, filters)

    def _contract_filter(self, query):
        if not (self.session.client.id is None or self._for_all()):
            query = query.filter(Contract.client_id == self.session.client.id)
        filters = {
            'FINISHED': lambda q: q.filter(Contract.status is True),
            'NOT_FINISHED': lambda q: q.filter(Contract.status is False),
            'WITH_EVENT': lambda q: q.filter(Contract.event.has()),
            'WITHOUT_EVENT': lambda q: q.filter(~Contract.event.has()),
        }
        return self._apply_filter(query, filters)

    def _event_filter(self, query):
        if not self._for_all() and self.session.connected_user.department_id == 2:
            query = query.filter(Event.support_contact_id == self.session.connected_user.id)
        filters = {
            'WITH_SUPPORT': lambda q: q.filter(Event.support_contact.has()),
            'WITHOUT_SUPPORT': lambda q: q.filter(~Event.support_contact.has()),
            'WITH_DATE_START': lambda q: q.filter(Event.date_start.has()),
            'WITHOUT_DATE_START': lambda q: q.filter(~Event.date_start.has()),
            'WITH_DATE_STOP': lambda q: q.filter(Event.date_stop.has()),
            'WITHOUT_DATE_STOP': lambda q: q.filter(~Event.date_stop.has()),
        }
        return self._apply_filter(query, filters)

    def _apply_filter(self, query, filters):
        if self.session.filter in filters:
            query = filters[self.session.filter](query)
        query = self._apply_join(query)
        return query

    def _apply_join(self, query):
        if not self._for_all() and self.session.connected_user.department_id == 1:
            if self.session.model == 'CONTRACT':
                query = query.join(Client).filter(Client.commercial_contact_id == self.session.connected_user.id)
            if self.session.model == 'EVENT' and self.session.action != 'ADD':
                query = query.join(Contract)
        return query

    def _for_all(self):
        return self.session.want_all

    def _fill_missing_field(self, model):
        match model:
            case 'USER':
                pass
            case 'CLIENT':
                self.session.client.commercial_contact_id = self.session.connected_user.id
            case 'CONTRACT':
                self.session.contract.client_id = self.session.client.id
            case 'EVENT':
                self.session.event.contract_id = self.session.contract.id
                if self.session.user.id is not None:
                    self.session.event.support_contact_id = self.session.user.id
        return None

    def _get_model(self, model):
        model_table = {
            'USER': EpicUser,
            'CLIENT': Client,
            'CONTRACT': Contract,
            'EVENT': Event
        }
        return model_table[model]

    def _get_filter_method(self, model):
        method_filter = {
            'USER': self._user_filter,
            'CLIENT': self._client_filter,
            'CONTRACT': self._contract_filter,
            'EVENT': self._event_filter
        }
        return method_filter[model]
