import jwt
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
        assert authentication.generate_token(1) is True
        assert 'TOKEN' in written
        decoded = jwt.decode(written['TOKEN'], 'my_secret_key', algorithms=['HS256'])
        assert decoded['employee_number'] == 1
        assert datetime.fromtimestamp(decoded['exp']) > datetime.now()
        assert datetime.fromtimestamp(decoded['exp']) < datetime.now() + timedelta(hours=4)

    def make_token(self, secret, exp):
        payload = {
            'employee_number': 1,
            'exp': exp
        }
        return jwt.encode(payload=payload, key=secret, algorithm='HS256')

    def test_check_token_valid(self, monkeypatch, authentication):
        secret = 'my_secret_key'
        token = self.make_token(secret=secret, exp=datetime.utcnow() + timedelta(hours=1))
        monkeypatch.setattr(
            target='controllers.authentication.get_key',
            name=lambda path, key: secret if key == 'SECRET_KEY' else token
        )
        assert authentication.check_token() == 1
