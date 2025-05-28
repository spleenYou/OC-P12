class Test_controller:
    def test_first_launch_without_user(self, controller_no_user, epic_user_information, monkeypatch):
        inputs = iter([
            epic_user_information['name'],
            epic_user_information['email'],
            epic_user_information['employee_number'],
            epic_user_information['department_id']
        ])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('views.prompt.getpass', lambda prompt: epic_user_information['password'])
        ctrl, db = controller_no_user
        ctrl.first_launch()
        assert db.user_created is True
