from argon2 import PasswordHasher


class Controller:
    def __init__(self, prompt, show, db):
        self.prompt = prompt()
        self.show = show()
        self.db = db()
        self._user_logged = False
        self.user_id = None

    def first_launch(self):
        if not self.db.has_epic_users():
            self.show.first_launch()
            self.create_user()
        return None

    def user_is_logged(self):
        if not self._user_logged:
            email = self.prompt.for_email()
            password = self.prompt.for_password()
            if self.db.user_exists(email, password):
                self.show.logged_ok()
                self._user_logged = True
            else:
                self.show.logged_nok()
        return self._user_logged

    def create_user(self):
        name = self.prompt.for_name()
        email = self.prompt.for_email()
        password = self.prompt.for_password()
        employee_number = self.prompt.for_employee_number()
        department_id = self.prompt.for_department(self.db.get_department_list())
        if self.db.add_user(name, email, password, employee_number, department_id):
            # Show a message
            return True
        # Show a message if not
        return False

    def hash_password(self, password):
        return PasswordHasher(
            time_cost=4,
            memory_cost=65536,
            parallelism=1,
            hash_len=32,
            salt_len=16
        ).hash(password)

    def password_verification(self, password, hash_password):
        try:
            return PasswordHasher(
                time_cost=4,
                memory_cost=65536,
                parallelism=1,
                hash_len=32,
                salt_len=16
            ).verify(hash_password, password)
        except Exception:
            return False
