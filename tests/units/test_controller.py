class Test_controller:
    def test_start_without_login_and_logged_ok(
            self,
            controller_without_login,
            epic_user_information,
            monkeypatch,
            capsys):
        inputs = iter(
            [
                epic_user_information['email'],
                epic_user_information['name'],
                epic_user_information['employee_number']
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        inputsPwd = iter(
            [
                epic_user_information['password'],
                epic_user_information['password']
            ]
        )
        monkeypatch.setattr('views.prompt.getpass', lambda prompt: next(inputsPwd))
        controller_without_login.start()
        captured = capsys.readouterr()
        assert 'Welcome on Epic Event !' in captured.out
        assert 'Premier lancement. Cr\xe9ation du premier utilisateur' in captured.out

    def test_start_and_logged_ok(self, controller, epic_user_information, monkeypatch, capsys):
        inputs = iter(
            [
                epic_user_information['name'],
                epic_user_information['employee_number']
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        inputsPwd = iter(
            [
                epic_user_information['password'],
                epic_user_information['password']
            ]
        )
        monkeypatch.setattr('views.prompt.getpass', lambda prompt: next(inputsPwd))
        controller.start()
        captured = capsys.readouterr()
        assert 'Welcome on Epic Event !' in captured.out
        assert 'Premier lancement. Cr\xe9ation du premier utilisateur' in captured.out

    def test_start_and_logged_fail(self, controller, epic_user_information, monkeypatch, capsys):
        inputs = iter(
            [
                epic_user_information['name'],
                epic_user_information['employee_number']
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        inputsPwd = iter(
            [
                epic_user_information['password'],
                epic_user_information['password'] + "e"
            ]
        )
        monkeypatch.setattr('views.prompt.getpass', lambda prompt: next(inputsPwd))
        controller.start()
        captured = capsys.readouterr()
        assert 'Sorry, your login/password are unknown' in captured.out

    def test_create_user_fail(self, controller, mysql_instance, department, epic_user_information, monkeypatch, capsys):
        inputs = iter([
            epic_user_information['name'],
            epic_user_information['employee_number'],
            epic_user_information['department_id'],
            epic_user_information['name'] + "e",
            epic_user_information['employee_number'] + 1,
            epic_user_information['department_id']
        ])
        inputsPwd = iter(
            [
                epic_user_information['password'],
                epic_user_information['password']
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('views.prompt.getpass', lambda prompt: next(inputsPwd))
        controller.create_user()
        result = controller.create_user()
        assert result is False

    def test_create_new_user(self, controller, mysql_instance, department, epic_user_information, monkeypatch, capsys):
        inputs = iter([
            epic_user_information['name'],
            epic_user_information['email'],
            epic_user_information['employee_number'],
            epic_user_information['department_id']
        ])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('views.prompt.getpass', lambda prompt: epic_user_information['password'])
        result = controller.create_user(ask_email=True)
        assert result is True
