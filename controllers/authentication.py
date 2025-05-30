import jwt
from datetime import datetime, timedelta
import secrets
from dotenv import set_key, load_dotenv, find_dotenv, get_key


class Authentication:
    def __init__(self):
        load_dotenv()
        self.dotenv_path = find_dotenv()

    def generate_secret_key(self):
        set_key(self.dotenv_path, 'SECRET_KEY', 'epicEvent-' + secrets.token_urlsafe(64))
        return True

    def generate_token(self, employee_number):
        set_key(
            self.dotenv_path,
            'TOKEN',
            jwt.encode(
                payload={
                    'employee_number': employee_number,
                    'exp': datetime.now() + timedelta(hours=2)
                },
                key=get_key(self.dotenv_path, 'SECRET_KEY')
            )
        )
        return True

    def check_token(self):
        try:
            token = jwt.decode(
                jwt=get_key(self.dotenv_path, 'TOKEN'),
                key=get_key(self.dotenv_path, 'SECRET_KEY'),
                algorithms=['HS256']
            )
            return token['employee_number']
        except Exception:
            return None
