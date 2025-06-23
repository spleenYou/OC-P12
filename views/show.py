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

    def show_content(self, content, border_style=config.normal_border_style):
        """Shows the content decorated

        Args:
            content (list): list of the content (str) to show
            align (str): Position of contents. Three possiblities left, center or right
        """
        panel = Panel(
            Align(content, align='center', style=config.normal_text_color),
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

        self.show_content(logo.logo)

    def session_information(self):
        if self.session.user.id is not None and self.session.status != 'LOGIN_OK':
            col_list = ['', '', '', '']
            row_list = [
                [
                    'Nom',
                    'Departement',
                    'Adresse mail',
                    'Numéro d\'employé'
                ],
                [
                    self.session.user.name,
                    self.session.user.department_name,
                    self.session.user.email,
                    str(self.session.user.employee_number)
                ]
            ]
            self.show_content(
                self._make_table(
                    col_list=col_list,
                    row_list=row_list,
                    justify='center',
                    show_header=False,
                    show_lines=True,
                    title='Utilisateur connecté')
            )

    def title(self):

        state = self.session.state.lower()
        border_style = getattr(config, state + '_' + 'border_style')
        text_color = getattr(config, state + '_' + 'text_color')
        self.show_content(
            f'[bold {text_color}]' + getattr(titles, state.upper())[self.session.status] + f'[/bold {text_color}]',
            border_style
        )

    def content(self):
        if self.session.state == 'GOOD':
            return None
        status = self._adapt_status_with_filter()
        simple_content = self._simple_content_view(status, self.session.state)
        if simple_content:
            self.show_content(Text(simple_content, justify='center'))
            return None
        complex_content = self._complex_content_view()
        if complex_content:
            self.show_content(complex_content)
        elif self.session.status.startswith(('ADD', 'UPDATE', 'DELETE', 'VIEW')):
            self.show_content(self._content_model_view())
        return None

    def show_select_user(self):
        users = self.db.get_user_list()
        col_list = ['N°', 'N° d\'employé', 'Nom', 'Email', 'Département']
        row_list = []
        for index, user in enumerate(users):
            row_list.append(
                [
                    str(index),
                    str(user.employee_number),
                    user.name,
                    user.email,
                    user.department_name
                ]
            )
        return self._make_table(col_list, row_list)

    def show_select_client(self):
        clients = self.db.get_client_list()
        col_list = ['N°', 'Nom de l\'entreprise', 'Contact']
        row_list = []
        for index, client in enumerate(clients):
            row_list.append(
                [
                    str(index),
                    client.company_name,
                    client.name
                ]
            )
        return self._make_table(col_list, row_list)

    def show_select_contract(self):
        contracts = self.db.get_contract_list()
        col_list = ['N°', 'Date de création', 'Montant total', 'Status']
        row_list = []
        for index, contract in enumerate(contracts):
            row_list.append(
                [
                    str(index),
                    contract.date_creation.strftime("%d %b %Y"),
                    str(contract.total_amount),
                    "Terminé" if contract.status else "En cours"
                ]
            )
        return self._make_table(col_list, row_list)

    def show_select_support_user(self):
        support_users = self.db.get_support_user_list()
        col_list = ['', '', '']
        row_list = []
        for index, user in enumerate(support_users):
            row_list.append([str(index), user.name, user.email])
        return self._make_table(col_list, row_list, show_header=False)

    def _make_table(self, col_list, row_list, justify='left', show_header=True, title=None, show_lines=False):
        table = Table(title=title, show_header=show_header, show_lines=show_lines)
        for col in col_list:
            table.add_column(col, justify=justify)
        for row in row_list:
            table.add_row(*row)
        return table

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
        content.add_row('nb de contrats', str(len(self.session.client.contracts)))
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
        support_user = 'Non défini'
        date_start = ''
        date_stop = ''
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
            if event.support_contact is None:
                event.support_contact = self.db.get_user_by_id(event.support_contact_id)
            support_user = f'{event.support_contact.name} - {event.support_contact.email}'
        date_start = event.date_start
        if date_start is not None:
            date_start = date_start.strftime("%d %b %Y")
        date_stop = event.date_stop
        if date_stop is not None:
            date_stop = date_stop.strftime("%d %b %Y")
        if event.attendees is not None:
            attendees = str(event.attendees)
        notes = event.notes
        content.add_row('Client', self.session.client.company_name + ' - ' + self.session.client.name)
        content.add_row('Commercial', (f"{self.session.client.commercial_contact.name} - "
                                       f"{self.session.client.commercial_contact.email}"))
        content.add_row('Support', support_user)
        content.add_row('Statut du contrat', 'Terminé' if self.session.contract.status else 'En cours')
        content.add_row('Reste à payer', str(self.session.contract.rest_amount))
        content.add_row('Lieu', event.location)
        content.add_row('Nombre de personnes', attendees)
        content.add_row('Date de début', date_start)
        content.add_row('Date de fin', date_stop)
        content.add_row('Notes', notes)
        content.add_row('Date de création', date_creation)
        return content

    def _simple_content_view(self, status, state):
        state_dict = getattr(contents, state, {})
        return state_dict.get(status)

    def _complex_content_view(self):
        match self.session.status:
            case 'SELECT_USER':
                return self.show_select_user()
            case 'SELECT_CLIENT':
                return self.show_select_client()
            case 'SELECT_CONTRACT':
                return self.show_select_contract()
            case 'SELECT_SUPPORT_USER':
                return self.show_select_support_user()
            case 'PERMISSION':
                return self.show_permissions()
            case _:
                return None

    def _content_model_view(self):
        status = self.session.status.split('_')
        content = Table(show_header=False, show_lines=True)
        content.add_column(justify='left')
        content.add_column(justify='left')
        show_methods = {
            'USER': self.show_user,
            'CLIENT': self.show_client,
            'CONTRACT': self.show_contract,
            'EVENT': self.show_event

        }
        method = show_methods.get(status[-1])
        return method(content)

    def _adapt_status_with_filter(self):
        if self.session.filter not in ['', 'FIRST_TIME', 'SECOND_TIME']:
            return self.session.status + '_' + self.session.filter
        return self.session.status
