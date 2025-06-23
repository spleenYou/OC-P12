import os
import datetime
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
                    'Numéro d\'employé',
                    'Nom',
                    'Departement',
                    'Adresse mail',
                ],
                [
                    str(self.session.user.employee_number),
                    self.session.user.name,
                    self.session.user.department_name,
                    self.session.user.email,
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
        status = self.session.status
        if 'ALL' in self.session.filter:
            status = status + 'S'
        self.show_content(
            f'[bold {text_color}]' + getattr(titles, state.upper())[status] + f'[/bold {text_color}]',
            border_style
        )

    def content(self):
        if self.session.state != 'GOOD':
            status = self._adapt_status_with_filter()
            simple_content = self._simple_content_view(status, self.session.state)
            if simple_content:
                self.show_content(Text(simple_content, justify='center'))
            else:
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

    def show_permissions(self):
        permissions = self.db.get_permissions()
        department_name = self.db.get_department_list()
        nb_dept = len(department_name)
        col_list = ['Command']
        row_list = []
        for perm in permissions:
            col_list.append(department_name[int(perm.department_id) - 1])
        for perm in config.permission_table:
            perms = ['X' if getattr(permissions[i], perm) else '' for i in range(nb_dept)]
            if perm == 'update_event':
                perms[2] = '*'
            perm = perm.replace('_', ' ')
            row_list.append([perm] + perms)
        table = self._make_table(col_list, row_list, justify='center', show_lines=True)
        note = Text(
            '* : L\'équipe management peut seulement mettre à jour\nle contact support d\'un évènement',
            justify='center'
        )
        return Group(table, '', note)

    def show_user(self):
        department_list = self.db.get_department_list()
        datas = [
            ('Nom', self.session.new_user.name or ''),
            ('Email', self.session.new_user.email or ''),
            ('Numéro d\'employé', (str(self.session.new_user.employee_number)
                                   if self.session.new_user.employee_number else '')),
            ('Département', (department_list[self.session.new_user.department_id - 1]
                             if self.session.new_user.department_id else '')),
            ('Date de création', self._format_date(self.session.new_user.date_creation or datetime.datetime.now())),
        ]
        return [[label, value] for label, value in datas]

    def show_client(self):
        datas = [
            ('Nom de l\'entreprise', self.session.client.company_name or ''),
            ('Nom du contact', self.session.client.name or ''),
            ('Email', self.session.client.email or ''),
            ('Téléphone', self.session.client.phone or ''),
            ('Commercial', self._get_commercial_info()),
            ('nb de contrats', str(len(self.session.client.contracts))),
            ('Date de création', self._format_date(self.session.client.date_creation or datetime.datetime.now())),
            ('Dernière mise à jour', self._format_date(self.session.client.date_last_update)),
        ]
        return [[label, value] for label, value in datas]

    def show_contract(self):
        datas = [
            ('Client', self.session.client.company_name + ' - ' + self.session.client.name),
            ('Commercial', (f"{self.session.client.commercial_contact.name} - "
                            f"{self.session.client.commercial_contact.email}")),
            ('Montant total', str(self.session.contract.total_amount or '0')),
            ('Reste à payer', str(self.session.contract.rest_amount or '0')),
            ('Statut', self._get_contract_status(self.session.contract)),
            ('Date de création', self._format_date(self.session.contract.date_creation or datetime.datetime.now()))
        ]
        return [[label, value] for label, value in datas]

    def show_event(self):
        event = self._select_event()
        datas = [
            ('Client', self.session.client.company_name + ' - ' + self.session.client.name),
            ('Commercial', (f"{self.session.client.commercial_contact.name} - "
                            f"{self.session.client.commercial_contact.email}")),
            ('Support', self._get_support_user_info(event)),
            ('Statut du contrat', 'Terminé' if self.session.contract.status else 'En cours'),
            ('Reste à payer', str(self.session.contract.rest_amount)),
            ('Lieu', event.location),
            ('Nombre de personnes', str(event.attendees) if event.attendees else ''),
            ('Date de début', self._format_date(event.date_start)),
            ('Date de fin', self._format_date(event.date_stop)),
            ('Notes', event.notes or ''),
            ('Date de création', self._format_date(event.date_creation or datetime.datetime.now())),
        ]
        return [[label, value] for label, value in datas]

    def show_users(self):
        user_list = self.db.get_user_list()
        datas = []
        for user in user_list:
            datas.append(
                [
                    user.employee_number,
                    user.name,
                    user.department_name,
                    user.email,
                    self._format_date(user.date_creation),
                ]
            )
        return datas

    def show_clients(self):
        client_list = self.db.get_client_list()
        datas = []
        for client in client_list:
            datas.append(
                [
                    client.company_name,
                    client.name,
                    client.email,
                    client.phone,
                    self._format_date(client.date_last_update),
                    self._format_date(client.date_creation),
                ]
            )
        return datas

    def show_contracts(self):
        contract_list = self.db.get_contract_list()
        datas = []
        for contract in contract_list:
            datas.append(
                [
                    contract.client.company_name,
                    str(contract.total_amount),
                    str(contract.rest_amount),
                    self._get_contract_status(contract),
                    self._format_date(contract.date_creation),
                ]
            )
        return datas

    def show_events(self):
        event_list = self.db.get_event_list()
        datas = []
        for event in event_list:
            datas.append(
                [
                    event.contract.client.company_name,
                    str(event.contract.total_amount),
                    event.location,
                    str(event.attendees),
                    self._format_date(event.date_start),
                    self._format_date(event.date_stop),
                    self._format_date(event.date_creation),
                ]
            )
        return datas

    def _get_commercial_info(self):
        if self.session.client.commercial_contact_id is None:
            return f'{self.session.user.name} - {self.session.user.email}'
        return f'{self.session.client.commercial_contact.name} - {self.session.client.commercial_contact.email}'

    def _get_support_user_info(self, event):
        if event.support_contact_id is None:
            return 'Non défini'
        if event.support_contact is None:
            event.support_contact = self.db.get_user_by_id(event.support_contact_id)
        return f'{event.support_contact.name} - {event.support_contact.email}'

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
        model_status = self.session.status.split('_')[-1]
        show_methods_one = {
            'USER': self.show_user,
            'CLIENT': self.show_client,
            'CONTRACT': self.show_contract,
            'EVENT': self.show_event,
            'USERS': self.show_users,
            'CLIENTS': self.show_clients,
            'CONTRACTS': self.show_contracts,
            'EVENTS': self.show_events
        }
        col_list = ['', '']
        show_header = False
        if 'ALL' in self.session.filter:
            show_header = True
            model_status = model_status + 'S'
            col_list = getattr(config, 'col_' + model_status.lower())
        row_list = show_methods_one.get(model_status)()
        return self._make_table(col_list, row_list, show_header=show_header, show_lines=True, justify='center')

    def _adapt_status_with_filter(self):
        if self.session.filter not in ['', 'FIRST_TIME', 'SECOND_TIME'] and 'ALL' not in self.session.filter:
            return self.session.status + '_' + self.session.filter
        return self.session.status

    def _make_table(self, col_list, row_list, justify='left', show_header=True, title=None, show_lines=False):
        table = Table(title=title, show_header=show_header, show_lines=show_lines)
        for col in col_list:
            table.add_column(col, justify=justify)
        for row in row_list:
            table.add_row(*row)
        return table

    def _select_event(self):
        if self.session.status == 'ADD_EVENT':
            return self.session.event
        return self.session.contract.event

    def _get_contract_status(self, contract):
        if contract.status:
            return 'Terminé'
        return 'En cours'

    def _format_date(self, date):
        return date.strftime('%d %b %Y') if date else ''
