class TestPermission:
    def test_add_client(self, permissions):
        assert permissions.add_client(1) is True
        assert permissions.add_client(2) is False
        assert permissions.add_client(3) is False

    def test_update_client(self, permissions):
        assert permissions.update_client(1) is True
        assert permissions.update_client(2) is False
        assert permissions.update_client(3) is False

    def test_delete_client(self, permissions):
        assert permissions.delete_client(1) is True
        assert permissions.delete_client(2) is False
        assert permissions.delete_client(3) is False

    def test_add_contract(self, permissions):
        assert permissions.add_contract(1) is False
        assert permissions.add_contract(2) is False
        assert permissions.add_contract(3) is True

    def test_update_contract(self, permissions):
        assert permissions.update_contract(1) is True
        assert permissions.update_contract(2) is False
        assert permissions.update_contract(3) is True

    def test_delete_contract(self, permissions):
        assert permissions.delete_contract(1) is True
        assert permissions.delete_contract(2) is False
        assert permissions.delete_contract(3) is True

    def test_add_event(self, permissions):
        assert permissions.add_event(1) is True
        assert permissions.add_event(2) is False
        assert permissions.add_event(3) is False

    def test_update_event(self, permissions):
        assert permissions.update_event(1) is False
        assert permissions.update_event(2) is True
        assert permissions.update_event(3) is False

    def test_delete_event(self, permissions):
        assert permissions.delete_event(1) is True
        assert permissions.delete_event(2) is True
        assert permissions.delete_event(3) is False

    def test_add_user(self, permissions):
        assert permissions.add_user(1) is False
        assert permissions.add_user(2) is False
        assert permissions.add_user(3) is True

    def test_update_user(self, permissions):
        assert permissions.update_user(1) is False
        assert permissions.update_user(2) is False
        assert permissions.update_user(3) is True

    def test_delete_user(self, permissions):
        assert permissions.delete_user(1) is False
        assert permissions.delete_user(2) is False
        assert permissions.delete_user(3) is True

    def test_update_support_on_event(self, permissions):
        assert permissions.update_support_on_event(1) is False
        assert permissions.update_support_on_event(2) is False
        assert permissions.update_support_on_event(3) is True
