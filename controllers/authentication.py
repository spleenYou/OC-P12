import os
import jwt
from datetime import datetime, timedelta, timezone
import secrets
from argon2 import PasswordHasher
from dotenv import set_key, load_dotenv, find_dotenv


class Authentication:
    """Handle the authentication

    Args:
        session (obj): Session object
    """

    def __init__(self, session):
        self.password_hasher = PasswordHasher(
            time_cost=int(os.getenv('TIME_COST')),
            memory_cost=int(os.getenv('MEMORY_COST')),
            parallelism=int(os.getenv('PARALLELISM')),
            hash_len=int(os.getenv('HASH_LEN')),
            salt_len=int(os.getenv('SALT_LEN'))
        )
        self.session = session

    def generate_secret_key(self):
        "Generate a secret key for the password encryption and set it in the .env file"

        set_key(find_dotenv(), 'SECRET_KEY', 'epicEvent-' + secrets.token_urlsafe(64))
        load_dotenv(override=True)
        return True

    def generate_token(self):
        "Generate a token for the user session with a time expiration"

        self.session.token = jwt.encode(
            payload={'exp': datetime.now(tz=timezone.utc) + timedelta(hours=5)},
            key=os.getenv('SECRET_KEY')
        )
        return True

    def check_token(self):
        "Verify the validity of the token"

        try:
            jwt.decode(
                jwt=self.session.token,
                key=os.getenv('SECRET_KEY'),
                algorithms=['HS256']
            )
            return True
        except Exception:
            return False

    def hash_password(self, password):
        """Hash the password

        Args:
            password (str)

        Returns:
            (str): the hashed password
        """

        return self.password_hasher.hash(password)

    def check_password(self, password, hashed_password):
        """Check if the password and the hashed password are same

        Args:
            password (str): the password enter by user
            hash_password (str): the hashed password store in the db

        Returns:
            (bool): the result of the check between password and hashed_password or False if a Exception is raised
        """

        try:
            return self.password_hasher.verify(hashed_password, password)
        except Exception:
            return False
