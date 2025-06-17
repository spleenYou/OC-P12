import jwt
import re
from datetime import datetime, timedelta


class TestAuthentication:
    def test_generate_secret_key(self, authentication):
        assert authentication.generate_secret_key() is True

    def test_generate_token(self, authentication, monkeypatch):
        written = {}
        monkeypatch.setattr(
            target='controllers.authentication.get_key',
            name=lambda path, key: 'my_secret_key'
        )

        def fake_set_key(dotenv_path, key, value):
            written[key] = value
            return True

        monkeypatch.setattr(
            target='controllers.authentication.set_key',
            name=fake_set_key
        )
        assert authentication.generate_token() is True
        assert authentication.session.token is not None
        decoded = jwt.decode(authentication.session.token, 'my_secret_key', algorithms=['HS256'])
        assert datetime.fromtimestamp(decoded['exp']) > datetime.now()
        assert datetime.fromtimestamp(decoded['exp']) < datetime.now() + timedelta(hours=10)

    def test_check_token_valid(self, monkeypatch, authentication, secret, token):
        monkeypatch.setattr(
            target='controllers.authentication.get_key',
            name=lambda path, key: secret
        )
        authentication.session.token = token
        assert authentication.check_token() is True

    def test_check_token_valid_fail(self, monkeypatch, authentication, secret, invalid_token):
        monkeypatch.setattr(
            target='controllers.authentication.get_key',
            name=lambda path, key: secret if key == 'SECRET_KEY' else invalid_token
        )
        assert authentication.check_token() is False

    def test_hash_password(self, authentication, management_user):
        hash_password = authentication.hash_password(management_user['password'])
        assert re.fullmatch(
            "[$]{1}argon2id[$]{1}v=19[$]{1}m=65536,t=4,p=1[$]{1}[+.\x00-9a-zA-Z]{22}[$]{1}[+.\x00-9a-zA-Z]{43}",
            hash_password
        ) is not None

    def test_password_verification(self, authentication, management_user):
        hash_password = authentication.hash_password(management_user['password'])
        assert authentication.check_password(management_user['password'], hash_password) is True

    def test_password_verification_fail(self, authentication, management_user):
        hash_password = authentication.hash_password(management_user['password'] + "e")
        assert authentication.check_password(management_user['password'], hash_password) is False
