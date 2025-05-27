from getpass import getpass


class Prompt:
    def __init__(self):
        pass

    def ask_user_loggin_information(self):
        login = input('Entrez votre login ? ')
        password = getpass('Entrez votre mot de passe : ')
        return login, password

    def for_name(self):
        name = input('Veuillez écrire votre nom : ')
        return name

    def for_email(self):
        email = input('Veuillez écrire votre email : ')
        return email

    def for_password(self):
        password = getpass('Veuillez écrire votre mot de passe : ')
        return password

    def for_employee_number(self):
        employee_number = input('Veuillez écrire votre numéro d\'employé : ')
        return employee_number

    def for_department(self, department_list):
        for index, department in enumerate(department_list):
            print(f'{index + 1} - {department}')
        department = input('Veuillez écrire votre le numéro de votre équipe : ')
        return department
