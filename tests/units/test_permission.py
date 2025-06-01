class TestPermission:
    def test_can_create_client(self, permissions):
        assert permissions.can_create_client(1) is True
        assert permissions.can_create_client(2) is False
        assert permissions.can_create_client(3) is False

    def test_can_update_client(self, permissions):
        assert permissions.can_update_client(1) is True
        assert permissions.can_update_client(2) is False
        assert permissions.can_update_client(3) is False

    def test_can_delete_client(self, permissions):
        assert permissions.can_delete_client(1) is True
        assert permissions.can_delete_client(2) is False
        assert permissions.can_delete_client(3) is False

    def test_can_create_contract(self, permissions):
        assert permissions.can_create_contract(1) is False
        assert permissions.can_create_contract(2) is False
        assert permissions.can_create_contract(3) is True

    def test_can_update_contract(self, permissions):
        assert permissions.can_update_contract(1) is True
        assert permissions.can_update_contract(2) is False
        assert permissions.can_update_contract(3) is True

    def test_can_delete_contract(self, permissions):
        assert permissions.can_delete_contract(1) is True
        assert permissions.can_delete_contract(2) is False
        assert permissions.can_delete_contract(3) is True

    def test_can_create_event(self, permissions):
        assert permissions.can_create_event(1) is True
        assert permissions.can_create_event(2) is False
        assert permissions.can_create_event(3) is False

    def test_can_update_event(self, permissions):
        assert permissions.can_update_event(1) is False
        assert permissions.can_update_event(2) is True
        assert permissions.can_update_event(3) is False

    def test_can_delete_event(self, permissions):
        assert permissions.can_delete_event(1) is True
        assert permissions.can_delete_event(2) is True
        assert permissions.can_delete_event(3) is False

    def test_can_create_user(self, permissions):
        assert permissions.can_create_user(1) is False
        assert permissions.can_create_user(2) is False
        assert permissions.can_create_user(3) is True

    def test_can_update_user(self, permissions):
        assert permissions.can_update_user(1) is False
        assert permissions.can_update_user(2) is False
        assert permissions.can_update_user(3) is True

    def test_can_delete_user(self, permissions):
        assert permissions.can_delete_user(1) is False
        assert permissions.can_delete_user(2) is False
        assert permissions.can_delete_user(3) is True

    def test_can_update_support_on_event(self, permissions):
        assert permissions.can_update_support_on_event(1) is False
        assert permissions.can_update_support_on_event(2) is False
        assert permissions.can_update_support_on_event(3) is True
