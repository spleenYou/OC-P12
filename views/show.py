import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.text import Text
import config.titles as titles
import config.simple_contents as simple_contents
import config.logo as logo
import config.config as config


class Show:
    def __init__(self, db, session):
        self.session = session
        self.db = db
        self.rich_console = Console(highlight=False)

    def display(self, content=None, align='center'):
        """Manages the display on the console

        Args:
            title (str): Title to show
            content (list): List of the text to show
            align (str): Position of the content. Three possiblities left, center or right
        """
        self.clear_screen()
        self.head_menu()
        self.session_information()
        self.title()
        self.content()

    def show_content(self, content, align, border_style):
        """Shows the content decorated

        Args:
            content (list): list of the content (str) to show
            align (str): Position of contents. Three possiblities left, center or right
        """
        panel = Panel(
            Align(content, align=align, style=config.text_color),
            width=config.common_width,
            padding=1,
            border_style=border_style
        )
        self.rich_console.print(panel)

    def clear_screen(self):
        "Clean the console for all os"

        command = "clear"
        if os.name in ("nt", "dos"):
            command = "cls"
        os.system(command)

    def head_menu(self):
        "Shows the name of the program decorated"

        self.show_content(logo.logo, 'center', config.border_style)

    def session_information(self):
        if self.session.user.id is not None and self.session.status != 'LOGIN_OK':
            content = Table(title='Utilisateur connecté', show_header=False, show_lines=True)
            content.add_column(justify='center')
            content.add_column(justify='center')
            content.add_column(justify='center')
            content.add_column(justify='center')
            content.add_row(
                'Nom',
                'Departement',
                'Adresse mail',
                'Numéro d\'employé'
            )
            content.add_row(
                self.session.user.name,
                self.session.user.department_name,
                self.session.user.email,
                str(self.session.user.employee_number)
            )
            self.show_content(content, 'center', config.border_style)

    def title(self):
        border_style = config.border_style
        status = self.session.status.split('_')
        if status[0] in ['BAD', 'UNKNOWN'] or status[-1] == 'FAILED':
            border_style = 'red'
        elif status[-1] == 'OK':
            border_style = 'green'
        text_color = config.text_color if border_style == config.border_style else border_style
        self.show_content(
            f'[bold {text_color}]' + getattr(titles, self.session.status) + f'[/bold {text_color}]',
            'center',
            border_style
        )

    def content(self):
        content = None
        align = 'center'
        if hasattr(simple_contents, self.session.status):
            self.show_content(
                Text(getattr(simple_contents, self.session.status), justify=align),
                align,
                config.border_style
            )
            return None
        match self.session.status:
            case 'SELECT_USER' | 'SELECT_USER_FOR_DELETE':
                users = self.db.get_user_list()
                content = Table(show_lines=True)
                content.add_column('N°', justify='left')
                content.add_column('Numéro employé', justify='left')
                content.add_column('Nom', justify='left')
                content.add_column('Email', justify='left')
                content.add_column('Département', justify='left')
                for index, user in enumerate(users):
                    content.add_row(
                        str(index),
                        str(user.employee_number),
                        user.name,
                        user.email,
                        user.department_name
                    )
            case ('SELECT_CLIENT' |
                  'SELECT_CLIENT_WITH_EVENT' |
                  'SELECT_CLIENT_WITHOUT_EVENT' |
                  'SELECT_CLIENT_WITH_CONTRACT'):
                clients = self.db.get_client_list()
                lines = [
                    f'{index} - {client.company_name} \\ {client.name}'
                    for index, client in enumerate(clients)
                ]
                content = "\n".join(lines)
            case 'SELECT_CONTRACT' | 'SELECT_CONTRACT_WITH_EVENT' | 'SELECT_CONTRACT_WITHOUT_EVENT':
                if self.session.status == 'SELECT_CONTRACT':
                    contracts = self.session.client.contracts
                else:
                    contracts = self.db.get_contract_list()
                lines = [
                    f'{index} - {contract.date_creation.strftime("%d %b %Y")} \\ '
                    f'{contract.total_amount} \\ '
                    f'{"Terminé" if contract.status else "En cours"}'
                    for index, contract in enumerate(contracts)
                ]
                content = "\n".join(lines)
            case 'SELECT_SUPPORT_USER':
                support_users = self.db.get_support_user_list()
                content = Table(show_header=False)
                content.add_column(justify='left')
                content.add_column(justify='left')
                content.add_column(justify='left')
                for index, user in enumerate(support_users):
                    content.add_row(str(index), user.name, user.email)
            case 'ADD_USER_FAILED':
                content = 'Utilisateur non enregistré'
                if self.db.number_of_user() == 0:
                    content = content + ('\nIl faut au moins un utilisateur pour utiliser l\'application\n'
                                         'Fermeture de l\'application')
            case 'PERMISSION':
                permissions_table = [
                    'add_user', 'update_user', 'delete_user',
                    'add_client', 'update_client', 'delete_client',
                    'add_contract', 'update_contract', 'delete_contract',
                    'add_event', 'update_event', 'delete_event',
                ]
                permissions = self.db.get_permissions()
                department_name = self.db.get_department_list()
                content = Table(show_lines=True)
                content.add_column("    Command", justify='left')
                for perm in permissions:
                    content.add_column(department_name[int(perm.department_id) - 1], justify='center')
                for perm in permissions_table:
                    commercial_perm = ''
                    support_perm = ''
                    management_perm = ''
                    if eval('permissions[0].' + perm):
                        commercial_perm = 'X'
                    if eval('permissions[1].' + perm):
                        support_perm = 'X'
                    if eval('permissions[2].' + perm):
                        management_perm = 'X'
                    if perm == 'update_event':
                        management_perm = '*'
                    perm = perm.replace('_', ' ')
                    content.add_row(perm, commercial_perm, support_perm, management_perm)
                content = '* : Le management peut mettre à jour le contact support d\'un évènement'

        status = self.session.status.split('_')
        if (status[0] in ['ADD', 'UPDATE', 'VIEW', 'DELETE'] and
                status[-1] in ['USER', 'CLIENT', 'CONTRACT', 'EVENT']):
            content = Table(show_header=False, show_lines=True)
            content.add_column(justify='left')
            content.add_column(justify='left')
            if status[-1] == 'USER':
                department_name = ''
                if self.session.new_user.department_id is not None:
                    department_name = self.db.get_department_list()[self.session.new_user.department_id - 1]
                employee_number = self.session.new_user.employee_number or ''
                content.add_row('Nom', self.session.new_user.name or '')
                content.add_row('Email', self.session.new_user.email or '')
                content.add_row('Numéro d\'employé', str(employee_number))
                content.add_row('Département', department_name)
            elif status[-1] == 'CLIENT':
                if self.session.client.commercial_contact_id is not None:
                    commercial_name = self.session.user.name
                    commercial_email = self.session.user.email
                else:
                    commercial_name = self.session.user.name
                    commercial_email = self.session.user.email
                content.add_row('Nom de l\'entreprise', self.session.client.company_name or '')
                content.add_row('Nom du contact', self.session.client.name or '')
                content.add_row('Email', self.session.client.email or '')
                content.add_row('Téléphone', self.session.client.phone or '')
                content.add_row('Commercial', (f"{commercial_name} - {commercial_email}"))
            elif status[-1] == 'CONTRACT':
                content.add_row('Client', self.session.client.company_name + ' - ' + self.session.client.name)
                content.add_row('Commercial', (f"{self.session.client.commercial_contact.name} - "
                                               f"{self.session.client.commercial_contact.email}"))
                content.add_row('Montant total', str(self.session.contract.total_amount or '0'))
                content.add_row('Reste à payer', str(self.session.contract.rest_amount or '0'))
                content.add_row('Statut', 'Terminé' if self.session.contract.status else 'En cours')
            elif status[-1] == 'EVENT':
                support_user = None
                date_start = ''
                date_stop = ''
                location = ''
                attendees = ''
                notes = ''
                if self.session.status == 'ADD_USER':
                    event = self.session.event
                else:
                    event = self.session.contract.event
                if event is not None:
                    if event.support_contact_id is not None:
                        support_user = event.support_contact
                    date_start = event.date_start
                    if date_start is not None:
                        date_start = date_start.strftime("%d %b %Y")
                    date_stop = event.date_stop
                    if date_stop is not None:
                        date_stop = date_stop.strftime("%d %b %Y")
                    location = event.location
                    attendees = str(event.attendees)
                    notes = event.notes
                content.add_row('Client', self.session.client.company_name + ' - ' + self.session.client.name)
                content.add_row('Commercial', (f"{self.session.client.commercial_contact.name} - "
                                               f"{self.session.client.commercial_contact.email}"))
                content.add_row('Support',
                                (support_user.name if support_user else '') +
                                ' - ' +
                                support_user.email if support_user else '')
                content.add_row('Statut du contrat', 'Terminé' if self.session.contract.status else 'En cours')
                content.add_row('Reste à payer', f"{self.session.contract.rest_amount}")
                content.add_row('Lieu', location)
                content.add_row('Nombre de personnes', attendees)
                content.add_row('Date de début', date_start)
                content.add_row('Date de fin', date_stop)
                content.add_row('Notes', notes)
        if content:
            if isinstance(content, str):
                self.show_content(Text(content, justify=align), align, config.border_style)
            else:
                self.show_content(content, align, config.border_style)
