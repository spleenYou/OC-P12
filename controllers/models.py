from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Boolean, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Departments(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    users = relationship('EpicUser', back_populates='department')
    permissions = relationship('Permission', back_populates='department')


class EpicUser(Base):
    __tablename__ = 'epic_users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    employee_number = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)
    date_creation = Column(Date, default=func.current_date())
    department = relationship('Department', back_populates='users')
    clients = relationship('Client', back_populates='commercial_contact')
    contracts = relationship('Contract', back_populates='commercial')
    events = relationship('Event', back_populates='support_contact')


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    entreprise_name = Column(String(255))
    date_creation = Column(Date, default=func.current_date())
    date_last_update = Column(Date, default=func.current_date(), onupdate=func.current_date())
    commercial_contact_id = Column(Integer, ForeignKey('epic_user.id'), nullable=False)
    commercial_contact = relationship('EpicUser', back_populates='clients')
    contracts = relationship('Contract', back_populates='client')
    events = relationship('Event', back_populates='client')


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    commercial_id = Column(Integer, ForeignKey('epic_user.id'), nullable=False)
    total_amount = Column(Numeric(10, 2))
    rest_amount = Column(Numeric(10, 2))
    date_creation = Column(Date, default=func.current_date())
    status = Column(Boolean, default=False)
    client = relationship('Client', back_populates='contracts')
    commercial = relationship('EpicUser', back_populates='contracts')
    events = relationship('Event', back_populates='contract')


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey('contract.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    date_creation = Column(Date, default=func.current_date())
    date_stop = Column(Date)
    support_contact_id = Column(Integer, ForeignKey('epic_user.id'), nullable=False)
    location = Column(String(255))
    attendees = Column(Integer)
    notes = Column(Text)
    contract = relationship('Contract', back_populates='events')
    client = relationship('Client', back_populates='events')
    support_contact = relationship('EpicUser', back_populates='events')


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('department.id'), unique=True)
    create_client = Column(Boolean, default=False)
    update_client = Column(Boolean, default=False)
    delete_client = Column(Boolean, default=False)
    create_contract = Column(Boolean, default=False)
    update_contract = Column(Boolean, default=False)
    delete_contract = Column(Boolean, default=False)
    create_event = Column(Boolean, default=False)
    update_event = Column(Boolean, default=False)
    delete_event = Column(Boolean, default=False)
    create_user = Column(Boolean, default=False)
    update_user = Column(Boolean, default=False)
    delete_user = Column(Boolean, default=False)
    update_support_on_event = Column(Boolean, default=False)
    department = relationship('Department', back_populates='permissions')
