class Test_controller:
    def test_first_launch_without_user(self, controller_no_user, epic_user_information, monkeypatch, capsys):
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
        captured = capsys.readouterr()
        assert 'Premier lancement. Cr\xe9ation du premier utilisateur' in captured.out

    def test_user_is_logged_fail(self, controller, epic_user_information, monkeypatch, capsys):
        monkeypatch.setattr('builtins.input', lambda _: epic_user_information['email'])
        monkeypatch.setattr('views.prompt.getpass', lambda prompt: epic_user_information['password'])
        assert controller.user_is_logged() is False
        captured = capsys.readouterr()
        assert "Sorry, your login/password are unknown" in captured.out

    def test_user_is_logged(self, mysql_instance, controller, epic_user_information, monkeypatch, capsys):
        mysql_instance.add_user(
            name=epic_user_information['name'],
            email=epic_user_information['email'],
            password=epic_user_information['password'],
            employee_number=epic_user_information['employee_number'],
            department_id=epic_user_information['department_id']
        )
        monkeypatch.setattr('builtins.input', lambda _: epic_user_information['email'])
        monkeypatch.setattr('views.prompt.getpass', lambda prompt: epic_user_information['password'])
        assert controller.user_is_logged() is True
        captured = capsys.readouterr()
        assert "Hello :)" in captured.out
