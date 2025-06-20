from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Boolean, Text, func, event, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.schema import DDL

Base = declarative_base()


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    users = relationship('EpicUser', back_populates='department')
    permissions = relationship('Permission', back_populates='department', uselist=False)


class EpicUser(Base):
    __tablename__ = 'epic_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=True)
    employee_number = Column(Integer, unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    date_creation = Column(DateTime, default=func.now())
    department = relationship('Department', back_populates='users')
    clients = relationship('Client', back_populates='commercial_contact')
    events = relationship('Event', back_populates='support_contact')

    @property
    def department_name(self):
        return self.department.name if self.department else None


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    company_name = Column(String(255))
    date_creation = Column(DateTime, default=func.now())
    date_last_update = Column(DateTime, default=func.now(), onupdate=func.now())
    commercial_contact_id = Column(Integer, ForeignKey('epic_users.id'), nullable=False)
    commercial_contact = relationship('EpicUser', back_populates='clients')
    contracts = relationship('Contract', back_populates='client', cascade='all, delete-orphan')


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    total_amount = Column(Numeric(10, 2))
    rest_amount = Column(Numeric(10, 2))
    date_creation = Column(DateTime, default=func.now())
    status = Column(Boolean, default=False)
    client = relationship('Client', back_populates='contracts')
    event = relationship('Event', back_populates='contract', uselist=False, cascade='all, delete-orphan')


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('contracts.id', ondelete='CASCADE'), nullable=False, unique=True)
    date_creation = Column(DateTime, default=func.now())
    date_start = Column(Date)
    date_stop = Column(Date)
    support_contact_id = Column(Integer, ForeignKey('epic_users.id'), nullable=True)
    location = Column(String(255))
    attendees = Column(Integer)
    notes = Column(Text)
    contract = relationship('Contract', back_populates='event')
    support_contact = relationship('EpicUser', back_populates='events')


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    department_id = Column(Integer, ForeignKey('departments.id'), unique=True)
    add_client = Column(Boolean, default=False)
    update_client = Column(Boolean, default=False)
    delete_client = Column(Boolean, default=False)
    add_contract = Column(Boolean, default=False)
    update_contract = Column(Boolean, default=False)
    delete_contract = Column(Boolean, default=False)
    add_event = Column(Boolean, default=False)
    update_event = Column(Boolean, default=False)
    delete_event = Column(Boolean, default=False)
    add_user = Column(Boolean, default=False)
    update_user = Column(Boolean, default=False)
    delete_user = Column(Boolean, default=False)
    department = relationship('Department', back_populates='permissions')


event.listen(
    Department.__table__,
    'after_create',
    DDL("""INSERT INTO departments (id, name) VALUES (1, "Commercial"), (2, "Support"), (3, "Management")""")
)


event.listen(
    Permission.__table__,
    'after_create',
    DDL("""INSERT INTO permissions
    (id, department_id, add_client, update_client, delete_client, add_contract, update_contract, delete_contract,
    add_event, update_event, delete_event, add_user, update_user, delete_user)
    VALUES
    (1, 1, True, True, True, False, True, True, True, False, True, False, False, False),
    (2, 2, False, False, False, False, False, False, False, True, True, False, False, False),
    (3, 3, False, False, False, True, True, True, False, True, False, True, True, True)""")
)
