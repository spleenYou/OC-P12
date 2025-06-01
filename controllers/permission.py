class Permission:
    def __init__(self, db):
        self.permissions = db.get_permissions()

    def can_create_client(self, permission_level):
        return self.permissions[permission_level - 1].create_client

    def can_update_client(self, permission_level):
        return self.permissions[permission_level - 1].update_client

    def can_delete_client(self, permission_level):
        return self.permissions[permission_level - 1].delete_client

    def can_create_contract(self, permission_level):
        return self.permissions[permission_level - 1].create_contract

    def can_update_contract(self, permission_level):
        return self.permissions[permission_level - 1].update_contract

    def can_delete_contract(self, permission_level):
        return self.permissions[permission_level - 1].delete_contract

    def can_create_event(self, permission_level):
        return self.permissions[permission_level - 1].create_event

    def can_update_event(self, permission_level):
        return self.permissions[permission_level - 1].update_event

    def can_delete_event(self, permission_level):
        return self.permissions[permission_level - 1].delete_event

    def can_create_user(self, permission_level):
        return self.permissions[permission_level - 1].create_user

    def can_update_user(self, permission_level):
        return self.permissions[permission_level - 1].update_user

    def can_delete_user(self, permission_level):
        return self.permissions[permission_level - 1].delete_user

    def can_update_support_on_event(self, permission_level):
        return self.permissions[permission_level - 1].update_support_on_event
