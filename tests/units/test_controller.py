class TestController:
    def test_start_without_user_and_no_registration(self, monkeypatch, controller, management_user, capsys):
        inputs = iter(
            [
                '',
                management_user['name'],
                management_user['email'],
                management_user['employee_number'],
                'n',
                ''
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('views.prompt.getpass', lambda _: management_user['password'])
        controller.start()
        captured = capsys.readouterr()
        assert 'Premier lancement de l\'application' in captured.out
        assert 'Utilisateur non enregistré' in captured.out

    def test_start_without_user_and_with_registration_and_login(self, monkeypatch, controller, management_user, capsys):
        inputs = iter(
            [
                '',
                management_user['name'],
                management_user['email'],
                management_user['employee_number'],
                'y',
                management_user['email'],
                '',
                ''
            ]
        )
        inputs_password = iter(
            [
                management_user['password'],
                management_user['password']
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('views.prompt.getpass', lambda _: next(inputs_password))
        controller.start()
        captured = capsys.readouterr()
        assert 'Premier lancement de l\'application' in captured.out
        assert 'Connexion' in captured.out
        assert 'Connexion réussie' in captured.out
        expected_text = f"Utilisateur : {management_user['name']} | Departement : {controller.db.get_department_name()}"
        assert expected_text in captured.out

    def test_start_with_user_and_login_failed(self, monkeypatch, controller, management_user, capsys):
        controller.session.new_user = management_user
        controller.db.add_user()
        controller.session.user = controller.db.get_user_information(management_user['email'])
        inputs = iter(
            [
                management_user['email'],
                ''
            ]
        )
        inputs_password = iter(
            [
                management_user['password'] + 'e'
            ]
        )
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        monkeypatch.setattr('views.prompt.getpass', lambda _: next(inputs_password))
        controller.start()
        captured = capsys.readouterr()
        print(captured)
        assert 'Erreur de connexion' in captured.out
        assert 'Vos identifiants sont inconnus' in captured.out
