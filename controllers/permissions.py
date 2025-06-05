class Check_Permission:
    def __init__(self, perms):
        self.permissions = perms
        self.permission_level = None

    def set_permission_level(self, permission_level):
        self.permission_level = permission_level - 1
        return None

    def add_client(self):
        return self.permissions[self.permission_level].add_client

    def update_client(self):
        return self.permissions[self.permission_level].update_client

    def delete_client(self):
        return self.permissions[self.permission_level].delete_client

    def add_contract(self):
        return self.permissions[self.permission_level].add_contract

    def update_contract(self):
        return self.permissions[self.permission_level].update_contract

    def delete_contract(self):
        return self.permissions[self.permission_level].delete_contract

    def add_event(self):
        return self.permissions[self.permission_level].add_event

    def update_event(self):
        return self.permissions[self.permission_level].update_event

    def delete_event(self):
        return self.permissions[self.permission_level].delete_event

    def add_user(self):
        return self.permissions[self.permission_level].add_user

    def update_user(self):
        return self.permissions[self.permission_level].update_user

    def delete_user(self):
        return self.permissions[self.permission_level].delete_user

    def update_support_on_event(self):
        return self.permissions[self.permission_level].update_support_on_event
