import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Mysql:
    def __init__(self):
        load_dotenv()
        self.session = None

    def create_engine(self):
        db_url = (f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
                  f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
        return create_engine(db_url)

    def create_sessions(self):
        if self.session is None:
            self.session = sessionmaker(bind=create_engine())
        return self.session

    def user_exists(self, login, password):
        return True
