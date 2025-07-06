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
    """Manages what is displayed on the console

    Args:
        db (obj): database object
        session (obj): session object
    """

    def __init__(self, db, session):
        self.session = session
        self.db = db
        self.rich_console = Console(highlight=False)

    def display(self):
        "Manages the display on the console"
        self._clear_screen()
        self._logo()
        self._session_information()
        self._title()
        self._content()

    def _show_content(self, content, border_style=config.normal_border_style):
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

    def _clear_screen(self):
        "Clean the console for all os"

        command = "clear"
        if os.name in ("nt", "dos"):
            command = "cls"
        os.system(command)

    def _logo(self):
        self._show_content(logo.logo)

    def _session_information(self):
        if self.session.connected_user.id is not None:
            row_list = [
                [
                    'Numéro d\'employé',
                    'Nom',
                    'Departement',
                    'Adresse mail',
                ],
                [
                    str(self.session.connected_user.employee_number),
                    self.session.connected_user.name,
                    self.session.connected_user.department_name,
                    self.session.connected_user.email,
                ]
            ]
            self._show_content(
                self._make_table(
                    col_name='session',
                    row_list=row_list,
                    justify='center',
                    show_header=False,
                    show_lines=True,
                    title='Utilisateur connecté')
            )

    def _title(self):
        state = self.session.state.lower()
        border_style = getattr(config, state + '_' + 'border_style')
        text_color = getattr(config, state + '_' + 'text_color')
        title = self._find_text('title')
        self._show_content(
            f'[bold {text_color}]' + title + f'[/bold {text_color}]',
            border_style
        )

    def _find_text(self, config_name):
        text = None
        config_module = {
            'title': titles,
            'simple_content': contents
        }
        available_titles = getattr(config_module[config_name], self.session.state)
        possibilities = [
            self.session.action + '_' + self.session.filter,
            self.session.action,
            self.session.action + '_' + self.session.model,
            self.session.state,
        ]
        for possibility in possibilities:
            if possibility in available_titles:
                text = possibility
                if self._is_for_all():
                    text = text + 'S'
                text = available_titles[text]
                break
        return text

    def _is_for_all(self):
        return self.session.want_all

    def _content(self):
        if self._content_needed():
            simple_content = self._find_text('simple_content')
            if simple_content:
                self._show_content(Text(simple_content, justify='center'))
            else:
                self._show_content(self._complex_content_view())
        return None

    def _show_select_user(self):
        users = self.db.get_list('USER')
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
        return self._make_table(col_name='select_user', row_list=row_list)

    def _show_select_client(self):
        clients = self.db.get_list('CLIENT')
        row_list = []
        for index, client in enumerate(clients):
            row_list.append(
                [
                    str(index),
                    client.company_name,
                    client.name
                ]
            )
        return self._make_table(col_name='select_client', row_list=row_list)

    def _show_select_contract(self):
        contracts = self.db.get_list('CONTRACT')
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
        return self._make_table(col_name='select_contract', row_list=row_list)

    def _show_permissions(self):
        permissions = self.db.get_permissions()
        department_name = self.db.get_department_list()
        nb_dept = len(department_name)
        row_list = []
        for perm in config.permission_table:
            perms = ['X' if getattr(permissions[i], perm) else '' for i in range(nb_dept)]
            if perm == 'update_event':
                perms[2] = '*'
            perm = perm.replace('_', ' ')
            row_list.append([perm] + perms)
        table = self._make_table(col_name='permissions', row_list=row_list, justify='center', show_lines=True)
        note = Text(
            '* : L\'équipe management peut seulement mettre à jour\nle contact support d\'un évènement',
            justify='center'
        )
        return Group(Align.center(table), '', note)

    def _get_row_user(self):
        department_list = self.db.get_department_list()
        datas = [
            ('Nom', self.session.user.name or ''),
            ('Email', self.session.user.email or ''),
            ('Numéro d\'employé', (str(self.session.user.employee_number)
                                   if self.session.user.employee_number else '')),
            ('Département', (department_list[self.session.user.department_id - 1]
                             if self.session.user.department_id else '')),
            ('Date de création', self._format_date(self.session.user.date_creation or datetime.datetime.now())),
        ]
        return datas

    def _get_row_client(self):
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
        return datas

    def _get_row_contract(self):
        datas = [
            ('Client', self.session.client.company_name + ' - ' + self.session.client.name),
            ('Commercial', (f"{self.session.client.commercial_contact.name} - "
                            f"{self.session.client.commercial_contact.email}")),
            ('Montant total', str(self.session.contract.total_amount or '0')),
            ('Reste à payer', str(self.session.contract.rest_amount or '0')),
            ('Statut', self._get_contract_status(self.session.contract)),
            ('Date de création', self._format_date(self.session.contract.date_creation or datetime.datetime.now()))
        ]
        return datas

    def _get_row_event(self):
        event = self._select_event()
        datas = [
            ('Client', self.session.client.company_name + ' - ' + self.session.client.name),
            ('Commercial', (f"{self.session.client.commercial_contact.name} - "
                            f"{self.session.client.commercial_contact.email}")),
            ('Support', self._get_support_user_info(event)),
            ('Statut du contrat', 'Terminé' if self.session.contract.status else 'En cours'),
            ('Reste à payer', f'{str(self.session.contract.rest_amount)}/{str(self.session.contract.total_amount)}'),
            ('Lieu', event.location),
            ('Nombre de personnes', str(event.attendees) if event.attendees else ''),
            ('Date de début', self._format_date(event.date_start)),
            ('Date de fin', self._format_date(event.date_stop)),
            ('Notes', event.notes or ''),
            ('Date de création', self._format_date(event.date_creation or datetime.datetime.now())),
        ]
        return datas

    def _get_row_users(self):
        user_list = self.db.get_list('USER')
        datas = []
        for user in user_list:
            datas.append(
                [
                    str(user.employee_number),
                    user.name,
                    user.department_name,
                    user.email,
                    self._format_date(user.date_creation),
                ]
            )
        return datas

    def _get_row_clients(self):
        client_list = self.db.get_list('CLIENT')
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

    def _get_row_contracts(self):
        contract_list = self.db.get_list('CONTRACT')
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

    def _get_row_events(self):
        event_list = self.db.get_list('EVENT')
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
            return f'{self.session.connected_user.name} - {self.session.connected_user.email}'
        return f'{self.session.client.commercial_contact.name} - {self.session.client.commercial_contact.email}'

    def _get_support_user_info(self, event):
        if event.support_contact_id is None:
            if self.session.user.id is None:
                return 'Non défini'
            else:
                return f'{self.session.user.name} - {self.session.user.email}'
        return f'{event.support_contact.name} - {event.support_contact.email}'

    def _complex_content_view(self):
        match self.session.action:
            case 'SELECT':
                return self._select_model()
            case 'PERMISSION':
                return self._show_permissions()
            case 'HELP':
                return self._show_help()
            case 'FILTER':
                return self._show_filter()
            case _:
                if self.session.model != '':
                    return self._content_model_view()
                return None

    def _select_model(self):
        match self.session.model:
            case 'USER':
                return self._show_select_user()
            case 'CLIENT':
                return self._show_select_client()
            case 'CONTRACT':
                return self._show_select_contract()

    def _show_help(self):
        row_list = [
            ('Action', 'ADD', 'UPDATE', 'VIEW', 'DELETE'),
            ('Catégorie', 'USER', 'CLIENT', 'CONTRACT', 'EVENT')
        ]
        table = self._make_table(
            col_name='help',
            row_list=row_list,
            show_lines=True,
            show_header=False,
            justify='center'
        )
        text = Text(config.text_help, justify='center')
        return Group(Align.center(table), '', text)

    def _show_filter(self):
        tables = [Text(config.filter_text, justify='center')]
        for category in config.filter:
            row_list = []
            for filter, text in config.filter[category].items():
                row_list.append((filter, text))
            tables.append(
                Align.center(
                    self._make_table(
                        col_name='filter',
                        row_list=row_list,
                        show_lines=True,
                        show_header=False,
                        justify='center',
                        title='COMMAND : ' + category
                    )
                )
            )
            tables.append('')
        text = Text('', justify='center')
        return Group(*tables)

    def _content_model_view(self):
        get_row_methods = {
            'USER': self._get_row_user,
            'CLIENT': self._get_row_client,
            'CONTRACT': self._get_row_contract,
            'EVENT': self._get_row_event,
            'USERS': self._get_row_users,
            'CLIENTS': self._get_row_clients,
            'CONTRACTS': self._get_row_contracts,
            'EVENTS': self._get_row_events
        }
        show_header = False
        model = self.session.model
        if self._is_for_all():
            show_header = True
            model = model + 'S'
        row_list = get_row_methods.get(model)()
        return self._make_table(
            col_name=model.lower(),
            row_list=row_list,
            show_header=show_header,
            show_lines=True,
            justify='center'
        )

    def _make_table(self, col_name, row_list, justify='left', show_header=True, title=None, show_lines=False):
        table = Table(title=title, show_header=show_header, show_lines=show_lines)
        for col in config.col[col_name]:
            table.add_column(col, justify=justify)
        for row in row_list:
            table.add_row(*row)
        return table

    def _select_event(self):
        if self.session.user_cmd == 'ADD_EVENT':
            return self.session.event
        return self.session.contract.event

    def _get_contract_status(self, contract):
        if contract.status:
            return 'Signé'
        return 'En attente'

    def _format_date(self, date):
        return date.strftime('%d %b %Y') if date else 'Non défini'

    def _content_needed(self):
        return (self.session.state != 'GOOD'
                and not ((self.session.action in config.crud_action)
                         and self.session.state == 'FAILED'
                         and self.session.filter != 'FIRST_TIME')
                and self.session.action not in config.action_without_content
                and not (self.session.action == 'CONNECTION' and self.session.state == 'NORMAL'))
