class Test_controller:
    def test_start_without_login_and_logged_ok(
            self,
            controller,
            epic_user_information,
            empty_user,
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
        controller.start(empty_user)
        captured = capsys.readouterr()
        assert 'Welcome on Epic Event !' in captured.out
        assert 'Premier lancement. Cr\xe9ation du premier utilisateur' in captured.out

    def test_start_with_login_and_logged_ok(self, controller, epic_user_information, empty_user, monkeypatch, capsys):
        inputs = iter(
            [
                epic_user_information['name'],
                epic_user_information['employee_number']
            ]
        )
        inputsPwd = iter(
            [
                epic_user_information['password'],
                epic_user_information['password']
            ]
        )
        user = empty_user
        user.email = epic_user_information['email']
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('views.prompt.getpass', lambda prompt: next(inputsPwd))
        controller.start(user)
        captured = capsys.readouterr()
        assert 'Welcome on Epic Event !' in captured.out
        assert 'Premier lancement. Cr\xe9ation du premier utilisateur' in captured.out

    def test_start_with_login_and_logged_failed(
            self,
            controller,
            epic_user_information,
            empty_user,
            monkeypatch,
            capsys):
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
        user = empty_user
        user.email = epic_user_information['email']
        monkeypatch.setattr('views.prompt.getpass', lambda prompt: next(inputsPwd))
        controller.start(user)
        captured = capsys.readouterr()
        assert 'Sorry, your login/password are unknown' in captured.out

    def test_add_user(self, controller, mysql_instance, epic_user_information, monkeypatch):
        inputs = iter([
            epic_user_information['name'],
            epic_user_information['email'],
            epic_user_information['employee_number'],
            epic_user_information['department_id']
        ])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('views.prompt.getpass', lambda prompt: epic_user_information['password'])
        result = controller.add_user(ask_email=True)
        assert result is True

    def test_add_user_failed(self, controller, mysql_instance, epic_user_information, empty_user, monkeypatch, capsys):
        controller.user_info = empty_user
        inputs = iter([
            epic_user_information['name'],
            epic_user_information['email'],
            epic_user_information['employee_number'],
            epic_user_information['department_id'],
            epic_user_information['name'] + "e",
            epic_user_information['email'],
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
        controller.add_user()
        result = controller.add_user()
        assert result is False
