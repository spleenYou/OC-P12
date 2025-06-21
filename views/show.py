import os
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.text import Text
import config.titles as titles
import config.simple_contents as contents
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
            Align(content, align=align, style=config.normal_text_color),
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

        self.show_content(logo.logo, 'center', config.normal_border_style)

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
            self.show_content(content, 'center', config.normal_border_style)

    def title(self):
        state = self.session.state.lower()
        border_style = getattr(config, state + '_' + 'border_style')
        text_color = getattr(config, state + '_' + 'text_color')
        self.show_content(
            f'[bold {text_color}]' + getattr(titles, state.upper())[self.session.status] + f'[/bold {text_color}]',
            'center',
            border_style
        )

    def content(self):
        if self.session.state == 'GOOD':
            return None
        content = None
        border_style = config.normal_border_style
        align = 'center'
        text = None
        status = self.session.status
        if self.session.filter not in ['', 'FIRST_TIME', 'SECOND_TIME']:
            status = status + '_' + self.session.filter
        if self.session.state == 'NORMAL' and status in contents.NORMAL:
            text = contents.NORMAL[status]
        if self.session.state == 'ERROR' and status in contents.ERROR:
            text = contents.ERROR[status]
        if self.session.state == 'FAILED' and status in contents.FAILED:
            text = contents.FAILED[status]
        if text:
            content = Text(text, justify=align)
        else:
            match self.session.status:
                case 'SELECT_USER':
                    content = self.show_select_user()
                case 'SELECT_CLIENT':
                    content = self.show_select_client()
                case 'SELECT_CONTRACT':
                    content = self.show_select_contract()
                case 'SELECT_SUPPORT_USER':
                    content = self.show_select_support_user()
                case 'PERMISSION':
                    content = self.show_permissions()
            status = self.session.status.split('_')
            if (status[0] in ['ADD', 'UPDATE', 'VIEW', 'DELETE'] and
                    status[-1] in ['USER', 'CLIENT', 'CONTRACT', 'EVENT']):
                content = Table(show_header=False, show_lines=True)
                content.add_column(justify='left')
                content.add_column(justify='left')
                if status[-1] == 'USER':
                    content = self.show_user(content)
                elif status[-1] == 'CLIENT':
                    content = self.show_client(content)
                elif status[-1] == 'CONTRACT':
                    content = self.show_contract(content)
                elif status[-1] == 'EVENT':
                    content = self.show_event(content)
        if content:
            if isinstance(content, str):
                self.show_content(Text(content, justify=align), align, border_style)
            else:
                self.show_content(content, align, border_style)

    def show_select_user(self):
        users = self.db.get_user_list()
        content = Table()
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
        return content

    def show_select_client(self):
        clients = self.db.get_client_list()
        content = Table()
        content.add_column('N°', justify='center')
        content.add_column('Nom de l\'entreprise', justify='center')
        content.add_column('Contact', justify='center')
        for index, client in enumerate(clients):
            content.add_row(
                str(index),
                client.company_name,
                client.name
                )
        return content

    def show_select_contract(self):
        contracts = self.db.get_contract_list()
        content = Table()
        content.add_column('N°', justify='center')
        content.add_column('Date de création', justify='center')
        content.add_column('Montant total', justify='center')
        content.add_column('Status', justify='center')
        for index, contract in enumerate(contracts):
            content.add_row(
                str(index),
                contract.date_creation.strftime("%d %b %Y"),
                str(contract.total_amount),
                "Terminé" if contract.status else "En cours")
        return content

    def show_select_support_user(self):
        support_users = self.db.get_support_user_list()
        content = Table(show_header=False)
        content.add_column(justify='left')
        content.add_column(justify='left')
        content.add_column(justify='left')
        for index, user in enumerate(support_users):
            content.add_row(str(index), user.name, user.email)
        return content

    def show_permissions(self):
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
        note = Text(
            '* : L\'équipe management peut seulement mettre à jour\nle contact support d\'un évènement',
            justify='center'
        )
        content = Group(content, '', note)
        return content

    def show_user(self, content):
        date_creation = ''
        if self.session.new_user.date_creation is not None:
            date_creation = self.session.new_user.date_creation.strftime("%d %b %Y")
        department_name = ''
        if self.session.new_user.department_id is not None:
            department_name = self.db.get_department_list()[self.session.new_user.department_id - 1]
        employee_number = self.session.new_user.employee_number or ''
        content.add_row('Nom', self.session.new_user.name or '')
        content.add_row('Email', self.session.new_user.email or '')
        content.add_row('Numéro d\'employé', str(employee_number))
        content.add_row('Département', department_name)
        content.add_row('Date de création', date_creation)
        return content

    def show_client(self, content):
        if self.session.client.commercial_contact_id is not None:
            commercial_name = self.session.user.name
            commercial_email = self.session.user.email
        else:
            commercial_name = self.session.user.name
            commercial_email = self.session.user.email
        date_creation = ''
        if self.session.client.date_creation is not None:
            date_creation = self.session.client.date_creation.strftime("%d %b %Y")
        date_last_update = ''
        if self.session.client.date_last_update is not None:
            date_last_update = self.session.client.date_last_update.strftime("%d %b %Y")
        content.add_row('Nom de l\'entreprise', self.session.client.company_name or '')
        content.add_row('Nom du contact', self.session.client.name or '')
        content.add_row('Email', self.session.client.email or '')
        content.add_row('Téléphone', self.session.client.phone or '')
        content.add_row('Commercial', (f"{commercial_name} - {commercial_email}"))
        content.add_row('Date de création', date_creation)
        content.add_row('Dernière mise à jour', date_last_update)
        return content

    def show_contract(self, content):
        date_creation = ''
        if self.session.contract.date_creation is not None:
            date_creation = self.session.contract.date_creation.strftime("%d %b %Y")
        content.add_row('Client', self.session.client.company_name + ' - ' + self.session.client.name)
        content.add_row('Commercial', (f"{self.session.client.commercial_contact.name} - "
                                       f"{self.session.client.commercial_contact.email}"))
        content.add_row('Montant total', str(self.session.contract.total_amount or '0'))
        content.add_row('Reste à payer', str(self.session.contract.rest_amount or '0'))
        content.add_row('Statut', 'Terminé' if self.session.contract.status else 'En cours')
        content.add_row('Date de création', date_creation)
        return content

    def show_event(self, content):
        support_user = None
        date_start = ''
        date_stop = ''
        location = ''
        attendees = ''
        notes = ''
        date_creation = ''
        if self.session.status == 'ADD_EVENT':
            event = self.session.event
        else:
            event = self.session.contract.event
        if event.date_creation is not None:
            date_creation = event.date_creation.strftime("%d %b %Y")
        if event.support_contact_id is not None:
            support_user = event.support_contact
        date_start = event.date_start
        if date_start is not None:
            date_start = date_start.strftime("%d %b %Y")
        date_stop = event.date_stop
        if date_stop is not None:
            date_stop = date_stop.strftime("%d %b %Y")
        location = event.location
        if event.attendees is not None:
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
        content.add_row('Reste à payer', str(self.session.contract.rest_amount))
        content.add_row('Lieu', location)
        content.add_row('Nombre de personnes', attendees)
        content.add_row('Date de début', date_start)
        content.add_row('Date de fin', date_stop)
        content.add_row('Notes', notes)
        content.add_row('Date de création', date_creation)
        return content
