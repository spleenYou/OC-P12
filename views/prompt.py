from getpass import getpass


class Prompt:
    def __init__(self, show):
        self.show = show

    def for_name(self):
        self.show.display()
        return input('Veuillez écrire votre nom : ')

    def for_client_name(self):
        self.show.display()
        return input('Veuillez écrire le nom du contact client : ')

    def for_entreprise_name(self):
        self.show.display()
        return input('Veuillez écrire le nom de l\'entreprise : ')

    def for_email(self):
        self.show.display()
        return input('Veuillez écrire votre email : ')

    def for_password(self):
        self.show.display()
        return getpass('Veuillez écrire votre mot de passe : ')

    def for_employee_number(self):
        self.show.display()
        return input('Veuillez écrire votre numéro d\'employé : ')

    def for_department(self, department_list):
        self.show.display()
        for index, department in enumerate(department_list):
            print(f'{index + 1} - {department}')
        return input('Veuillez écrire votre le numéro de votre équipe : ')

    def for_phone(self):
        self.show.display()
        return input('Veuillez écrire le numéro de téléphone du client : ')

    def for_total_amount(self):
        self.show.display()
        return input('Veuillez indiquer le montant total du contrat : ')

    def for_rest_amount(self):
        self.show.display()
        return input('Veuillez indiquer le reste à payer pour ce contrat : ')

    def for_select_client(self, client_list):
        self.show.display()
        print('Liste des clients')
        print('0 - Annuler')
        for index, client in enumerate(client_list):
            print(f'{index + 1} - {client.entreprise_name}')
        choice = input('Veuillez entrer le numéro du client : ')
        if choice:
            return client_list[choice - 1]
        return None

    def for_validation(self):
        self.show.display()
        choice = input('Souhaitez vous continuer ? (y/n)')
        if choice in ['y', 'Y']:
            return True
        return False
