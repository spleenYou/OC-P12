from getpass import getpass


class Prompt:
    def __init__(self, show):
        self.show = show

    def for_name(self):
        self.show.display()
        return input('Veuillez entrer le nom : ')

    def for_client_name(self):
        self.show.display()
        return input('Veuillez entrer le nom du contact client : ')

    def for_company_name(self):
        self.show.display()
        return input('Veuillez entrer le nom de l\'entreprise : ')

    def for_email(self):
        self.show.display()
        return input('Veuillez entrer votre email : ')

    def for_password(self):
        self.show.display()
        return getpass('Veuillez entrer votre mot de passe : ')

    def for_employee_number(self):
        self.show.display()
        return input('Veuillez entrer votre numéro d\'employé : ')

    def for_department(self, department_list):
        self.show.display()
        departments = ''
        for index, department in enumerate(department_list):
            departments = departments + f'{index + 1} : {department} | '
        return input(f'Veuillez entrer votre le numéro de votre équipe ({departments[:-3]}) : ')

    def for_phone(self):
        self.show.display()
        return input('Veuillez entrer le numéro de téléphone du client : ')

    def for_total_amount(self):
        self.show.display()
        return input('Veuillez indiquer le montant total du contrat : ')

    def for_rest_amount(self):
        self.show.display()
        return input('Veuillez indiquer le reste à payer pour ce contrat : ')

    def for_client(self):
        self.show.display()
        return input('Quel client souhaitez vous ? ')

    def for_validation(self):
        self.show.display()
        choice = input('Souhaitez vous continuer (y/n) ? ')
        if choice in ['y', 'Y']:
            return True
        return False

    def for_command(self):
        self.show.display()
        return input('> ')

    def for_user(self):
        self.show.display()
        return input('Quel utilisateur souhaitez vous modifier ? ')
