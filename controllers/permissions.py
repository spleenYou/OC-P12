class Permission:
    def __init__(self, db, session):
        self.permissions = db.get_permissions()
        self.session = session

    def add_client(self):
        return self.permissions[self.session.user.department_id - 1].add_client

    def update_client(self):
        return self.permissions[self.session.user.department_id - 1].update_client

    def delete_client(self):
        return self.permissions[self.session.user.department_id - 1].delete_client

    def add_contract(self):
        return self.permissions[self.session.user.department_id - 1].add_contract

    def update_contract(self):
        return self.permissions[self.session.user.department_id - 1].update_contract

    def delete_contract(self):
        return self.permissions[self.session.user.department_id - 1].delete_contract

    def add_event(self):
        return self.permissions[self.session.user.department_id - 1].add_event

    def update_event(self):
        return self.permissions[self.session.user.department_id - 1].update_event

    def delete_event(self):
        return self.permissions[self.session.user.department_id - 1].delete_event

    def add_user(self):
        return self.permissions[self.session.user.department_id - 1].add_user

    def update_user(self):
        return self.permissions[self.session.user.department_id - 1].update_user

    def delete_user(self):
        return self.permissions[self.session.user.department_id - 1].delete_user

    def update_support_on_event(self):
        return self.permissions[self.session.user.department_id - 1].update_support_on_event
