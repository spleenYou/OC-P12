import jwt
import re
from datetime import datetime, timedelta


class TestAuthentication:
    def test_generate_secret_key(self, authentication):
        assert authentication.generate_secret_key() is True

    def test_generate_token(self, authentication, monkeypatch, secret):
        monkeypatch.setenv('SECRET_KEY', secret)
        assert authentication.generate_token() is True
        assert authentication.session.token is not None
        decoded = jwt.decode(authentication.session.token, secret, algorithms=['HS256'])
        assert datetime.fromtimestamp(decoded['exp']) > datetime.now()
        assert datetime.fromtimestamp(decoded['exp']) < datetime.now() + timedelta(hours=10)

    def test_check_token_valid(self, monkeypatch, authentication, secret, token):
        monkeypatch.setenv('SECRET_KEY', secret)
        authentication.session.token = token
        assert authentication.check_token() is True

    def test_check_token_valid_fail(self, monkeypatch, authentication, secret, invalid_token):
        monkeypatch.setenv('SECRET_KEY', secret)
        assert authentication.check_token() is False

    def test_hash_password(self, authentication, password):
        hash_password = authentication.hash_password(password)
        assert re.fullmatch(
            "[$]{1}argon2id[$]{1}v=19[$]{1}m=65536,t=4,p=1[$]{1}[+.\x00-9a-zA-Z]{22}[$]{1}[+.\x00-9a-zA-Z]{43}",
            hash_password
        ) is not None

    def test_password_verification(self, authentication, password):
        hash_password = authentication.hash_password(password)
        assert authentication.check_password(password, hash_password) is True

    def test_password_verification_fail(self, authentication, password):
        hash_password = authentication.hash_password(password + "e")
        assert authentication.check_password(password, hash_password) is False
