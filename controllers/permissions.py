class Check_Permission:
    def __init__(self, perms):
        self.permissions = perms

    def add_client(self, permission_level):
        return self.permissions[permission_level - 1].add_client

    def update_client(self, permission_level):
        return self.permissions[permission_level - 1].update_client

    def delete_client(self, permission_level):
        return self.permissions[permission_level - 1].delete_client

    def add_contract(self, permission_level):
        return self.permissions[permission_level - 1].add_contract

    def update_contract(self, permission_level):
        return self.permissions[permission_level - 1].update_contract

    def delete_contract(self, permission_level):
        return self.permissions[permission_level - 1].delete_contract

    def add_event(self, permission_level):
        return self.permissions[permission_level - 1].add_event

    def update_event(self, permission_level):
        return self.permissions[permission_level - 1].update_event

    def delete_event(self, permission_level):
        return self.permissions[permission_level - 1].delete_event

    def add_user(self, permission_level):
        return self.permissions[permission_level - 1].add_user

    def update_user(self, permission_level):
        return self.permissions[permission_level - 1].update_user

    def delete_user(self, permission_level):
        return self.permissions[permission_level - 1].delete_user

    def update_support_on_event(self, permission_level):
        return self.permissions[permission_level - 1].update_support_on_event
