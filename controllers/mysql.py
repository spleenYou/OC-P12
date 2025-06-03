import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, EpicUser, Department, Permission
from argon2 import PasswordHasher
from controllers.authentication import Authentication
from controllers.permissions import Check_Permission
from sqlalchemy.exc import IntegrityError


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
        self.auth = Authentication()
        get_perms = self.get_permissions()
        self.perms = Check_Permission(get_perms)

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
            .filter(EpicUser.email == email).first()
        if (user_information is not None and self.password_verification(password, user_information.password)):
            return user_information
        return None

    def get_department_list(self):
        return [d[0] for d in self.session.query(Department.name).order_by(Department.id).all()]

    def add_in_db(self, element_to_add):
        try:
            self.session.add(element_to_add)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def get_permissions(self):
        return self.session.query(Permission).all()

    def hash_password(self, password):
        return self.password_hasher.hash(password)

    def password_verification(self, password, hash_password):
        try:
            return self.password_hasher.verify(hash_password, password)
        except Exception:
            return False
