import os
import jwt
from datetime import datetime, timedelta
import secrets
from argon2 import PasswordHasher
from dotenv import set_key, load_dotenv, find_dotenv, get_key


class Authentication:
    def __init__(self, session):
        load_dotenv()
        self.dotenv_path = find_dotenv()
        self.password_hasher = PasswordHasher(
            time_cost=int(os.getenv('TIME_COST')),
            memory_cost=int(os.getenv('MEMORY_COST')),
            parallelism=int(os.getenv('PARALLELISM')),
            hash_len=int(os.getenv('HASH_LEN')),
            salt_len=int(os.getenv('SALT_LEN'))
        )
        self.session = session

    def generate_secret_key(self):
        set_key(self.dotenv_path, 'SECRET_KEY', 'epicEvent-' + secrets.token_urlsafe(64))
        return True

    def generate_token(self):
        self.session.token = jwt.encode(
            payload={
                'permission_level': self.session.user['department_id'],
                'exp': datetime.now() + timedelta(hours=2)
            },
            key=get_key(self.dotenv_path, 'SECRET_KEY')
        )
        return True

    def check_token(self):
        try:
            jwt.decode(
                jwt=self.session.token,
                key=get_key(self.dotenv_path, 'SECRET_KEY'),
                algorithms=['HS256']
            )
            return True
        except Exception:
            return False

    def hash_password(self, password):
        return self.password_hasher.hash(password)

    def check_password(self, password, hash_password):
        try:
            return self.password_hasher.verify(hash_password, password)
        except Exception:
            return False
