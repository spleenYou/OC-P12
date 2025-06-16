from rich.prompt import Prompt, Confirm
from rich.console import Console
import sys


class Ask:
    def __init__(self, show, db):
        self.display = show.display
        self.db = db
        self.console = Console(file=sys.stdout, force_terminal=False)
        departments = ' | '.join(f'{i + 1} {d}' for i, d in enumerate(self.db.get_department_list()))
        self.PROMPTS = {
            'email': 'Veuillez entrer votre e-mail :',
            'password': 'Veuillez entrer votre mot de passe :',
            'name': 'Veuillez entrer le nom :',
            'employee_number': 'Veuillez entrer votre numéro d\'employé :',
            'department': f'Veuillez entrer votre le numéro de votre équipe ({departments}) :',
            'client_name': 'Veuillez entrer le nom du contact client :',
            'company_name': 'Veuillez entrer le nom de l\'entreprise :',
            'phone': 'Veuillez entrer le numéro de téléphone du client :',
            'total_amount': 'Veuillez indiquer le montant total du contrat :',
            'rest_amount': 'Veuillez indiquer le reste à payer pour ce contrat :',
            'location': 'Veuillez indiquer un lieu :',
            'notes': 'Veuillez écrire une note (optionnel) :',
            'attendees': 'Veuillez entrer le nombre de personnes présentes :',
            'date_start': 'Veuillez rentrer une date de début (jj/mm/aaaa) :',
            'date_stop': 'Veuillez rentrer une date de fin (jj/mm/aaaa) :',
            'contract_status': 'Veuillez entrer statut du contrat (En cours n / Terminé y) :',
            'user': 'Veuillez entrer le numéro d\'un utilisateur :',
            'support_user': 'Veuillez entrer le numéro d\'un utilisateur :',
            'client': 'Veuillez entrer le numéro d\'un client :',
            'contract': 'Veuillez entrer le numéro d\'un contrat :',
            'command': '> '
        }

    def thing(self, thing):
        self.display()
        text = '\n' + self.PROMPTS[thing]
        if thing == 'password':
            return Prompt.ask(text, password=True)
        return self.console.input(text)

    def validation(self):
        self.display()
        return Confirm.ask('[bold yellow]Souhaitez-vous continuer ?[/bold yellow]', default=True)
