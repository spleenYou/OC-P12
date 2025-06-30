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
        query = self.db_session.query(self._get_model(model))
        query = self._get_filter_method(model)(query)
        return query.count()

    def get_department_list(self):
        return [d[0] for d in self.db_session.query(Department.name).order_by(Department.id).all()]

    def add(self, model):
        self._fill_missing_field(model)
        return self._add_in_db(getattr(self.session, model))

    def update_password_user(self, email):
        count = self.db_session.query(EpicUser) \
                    .filter(EpicUser.email == email) \
                    .update({'password': self.auth.hash_password(self.session.connected_user.password)})
        self.db_session.commit()
        return count > 0

    def get(self, model, number):
        model_obj = self._get_model(model)
        query = self.db_session.query(model_obj).order_by(model_obj.id)
        query = self._get_filter_method(model)(query)
        return query.all()[number]

    def get_user_password(self, email):
        password = self.db_session.query(EpicUser) \
            .with_entities(EpicUser.password) \
            .filter(EpicUser.email == email).first()
        if password:
            return password[0]
        return None

    def delete(self, model):
        try:
            attr = getattr(self.session, model)
            self.db_session.delete(attr)
            result = attr in self.db_session.deleted
            self.db_session.commit()
            return result
        except Exception as ex:
            print(ex)
            self.db_session.rollback()
            return False

    def get_list(self, model):
        query = self.db_session.query(self._get_model(model))
        query = self._get_filter_method(model)(query)
        return query.all()

    def get_permissions(self):
        return self.db_session.query(Permission).all()

    def employee_number_exits(self, employee_number):
        return self.db_session.query(EpicUser).filter(EpicUser.employee_number == employee_number).first()

    def _add_in_db(self, element_to_add):
        try:
            self.db_session.add(element_to_add)
            self.db_session.commit()
            return True
        except IntegrityError as e:
            print(f'IntegrityError : {e}')
            self.db_session.rollback()
            return False

    def _clean_filter(self):
        return self.session.filter.replace('ALL_', '')

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
        filter = self._clean_filter()
        if filter in filters:
            query = filters[filter](query)
        return query

    def _for_all(self):
        return 'ALL' in self.session.filter

    def _fill_missing_field(self, model):
        match model:
            case 'user':
                pass
            case 'client':
                self.session.client.commercial_contact_id = self.session.connected_user.id
            case 'contract':
                self.session.contract.client_id = self.session.client.id
            case 'event':
                self.session.event.contract_id = self.session.contract.id
        return None

    def _get_model(self, model):
        model_table = {
            'user': EpicUser,
            'client': Client,
            'contract': Contract,
            'event': Event
        }
        return model_table[model]

    def _get_filter_method(self, model):
        method_filter = {
            'user': self._user_filter,
            'client': self._client_filter,
            'contract': self._contract_filter,
            'event': self._event_filter
        }
        return method_filter[model]
