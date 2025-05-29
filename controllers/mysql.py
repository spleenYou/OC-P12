import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, EpicUser, Department
from argon2 import PasswordHasher


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
            .with_entities(EpicUser.id, EpicUser.password) \
            .filter(EpicUser.email == email).first()
        if (user_information is not None and self.password_verification(password, user_information[1])):
            return user_information[0]
        return None

    def get_department_list(self):
        return [d[0] for d in self.session.query(Department.name).order_by(Department.id).all()]

    def add_user(self, name, email, password, employee_number, department_id):
        try:
            self.session.add(
                EpicUser(
                    name=name,
                    email=email,
                    password=self.hash_password(password),
                    employee_number=employee_number,
                    department_id=department_id
                )
            )
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            return False

    def hash_password(self, password):
        return self.password_hasher.hash(password)

    def password_verification(self, password, hash_password):
        try:
            return self.password_hasher.verify(hash_password, password)
        except Exception:
            return False
