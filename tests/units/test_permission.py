class TestPermission:
    def test_commercial_permissions(self, permissions, session):
        session.user.department_id = 1
        assert permissions.add_client() is True
        assert permissions.update_client() is True
        assert permissions.delete_client() is True
        assert permissions.add_contract() is False
        assert permissions.update_contract() is True
        assert permissions.delete_contract() is True
        assert permissions.add_event() is True
        assert permissions.update_event() is False
        assert permissions.delete_event() is True
        assert permissions.add_user() is False
        assert permissions.update_user() is False
        assert permissions.delete_user() is False
        assert permissions.update_support_on_event() is False

    def test_support_permissions(self, permissions, session):
        session.user.department_id = 2
        assert permissions.add_client() is False
        assert permissions.update_client() is False
        assert permissions.delete_client() is False
        assert permissions.add_contract() is False
        assert permissions.update_contract() is False
        assert permissions.delete_contract() is False
        assert permissions.add_event() is False
        assert permissions.update_event() is True
        assert permissions.delete_event() is True
        assert permissions.add_user() is False
        assert permissions.update_user() is False
        assert permissions.delete_user() is False
        assert permissions.update_support_on_event() is False

    def test_management_permissions(self, permissions, session):
        session.user.department_id = 3
        assert permissions.add_client() is False
        assert permissions.update_client() is False
        assert permissions.delete_client() is False
        assert permissions.add_contract() is True
        assert permissions.update_contract() is True
        assert permissions.delete_contract() is True
        assert permissions.add_event() is False
        assert permissions.update_event() is False
        assert permissions.delete_event() is False
        assert permissions.add_user() is True
        assert permissions.update_user() is True
        assert permissions.delete_user() is True
        assert permissions.update_support_on_event() is True
