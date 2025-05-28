import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, EpicUser, Department


class Mysql:
    def __init__(self):
        load_dotenv()
        self.engine = self.create_engine()
        Base.metadata.create_all(bind=self.engine)
        self.session = self.create_session()

    def create_engine(self):
        db_url = (f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
                  f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
        return create_engine(db_url)

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

    def has_epic_users(self):
        return self.session.query(EpicUser).count()

    def user_exists(self, email, password):
        user_id = self.session.query(EpicUser) \
            .with_entities(EpicUser.id) \
            .filter(EpicUser.email == email, EpicUser.password == password).count()
        if user_id:
            return user_id
        return None

    def get_department_list(self):
        return [d[0] for d in self.session.query(Department.name).all()]

    def add_user(self, name, email, password, employee_number, department_id):
        try:
            self.session.add(
                EpicUser(
                    name=name,
                    email=email,
                    password=password,
                    employee_number=employee_number,
                    department_id=department_id
                )
            )
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            return False
