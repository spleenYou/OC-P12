common_width = 120
normal_border_style = 'cyan'
error_border_style = 'red'
failed_border_style = 'dark_orange'
good_border_style = 'green'
normal_text_color = 'dark_orange3'
error_text_color = 'red'
failed_text_color = 'dark_orange'
good_text_color = 'green'
validation_text_color = 'yellow'
permission_table = [
    'add_user', 'update_user', 'delete_user',
    'add_client', 'update_client', 'delete_client',
    'add_contract', 'update_contract', 'delete_contract',
    'add_event', 'update_event', 'delete_event',
]
col_users = [
    'N° d\'employé',
    'Nom',
    'Département',
    'Adresse mail',
    'Date de création',
]
col_clients = [
    'Entreprise',
    'Contact',
    'Adresse mail',
    'Téléphone',
    'Dernière mise à jour',
    'Création',
]
col_contracts = [
    'Client',
    'Montant total',
    'Restant à payer',
    'Status',
    'Création',
]
col_events = [
    'Client',
    'Montant total',
    'Lieu',
    'Nb de personnes',
    'Début',
    'Fin',
    'Création',
]
select_status = {
    'user': 'SELECT_USER',
    'support': 'SELECT_USER',
    'client': 'SELECT_CLIENT',
    'contract': 'SELECT_CONTRACT',
}
is_nullable = [
    'notes',
    'date_start',
    'date_stop',
    'support_contact_id',
]
is_text = [
    'command',
    'name',
    'password',
    'client_name',
    'phone',
    'company_name',
    'location',
    'notes',
    'status'
]
is_date = [
    'date_start',
    'date_stop',
]
is_int = [
    'attendees',
    'employee_number',
    'department'
]
is_float = [
    'total_amount',
    'rest_amount',
]
is_email = [
    'email',
    'client_email'
]
user_attrs = [
    'name',
    'email',
    'department_id',
    'employee_number',
]
client_attrs = [
    'name',
    'email',
    'phone',
    'company_name',
    'date_last_update',
]
contract_attrs = [
    'total_amount',
    'rest_amount',
    'status',
]
event_attrs = [
    'date_start',
    'date_stop',
    'support_contact_id',
    'location',
    'attendees',
    'notes',
]
status_without_content = [
    'FORBIDDEN',
    'EXIT',
    'NO_CLIENT',
    'NO_CONTRACT',
    'NO_EVENT',
]
authorized_commands = ['HELP', 'EXIT', 'PERMISSION', 'RESET', 'FILTER']

filter = {
    'VIEW USER': {
        'COMMERCIAL': 'Voir un utilisateur du département commercial',
        'SUPPORT': 'Voir un utilisateur du département support',
        'MANAGEMENT': 'Voir un utilisateur du département management',
    },
    'VIEW CLIENT': {
        'WITH_CONTRACT': 'Voir un client qui a au moins un contrat',
        'WITHOUT_CONTRACT': 'Voir un client qui n\'a pas de contrat',
        'WITH_EVENT': 'Voir un client qui a un au moins un évènement',
        'WITHOUT_EVENT': 'Voir un client qui n\'a pas d\'évènement',
    },
    'VIEW CONTRACT': {
        'WITH_EVENT': 'Voir un contrat qui a un au moins un évènement',
        'WITHOUT_EVENT': 'Voir un contrat qui n\'a pas d\'évènement',
        'FINISHED': 'Voir un contrat qui est terminé',
        'NOT_FINISHED': 'Voir un contrat qui n\'est pas terminé',
    },
    'VIEW EVENT': {
        'WITH_SUPPORT': 'Voir un évènement qui a un utilisateur support',
        'WITHOUT_SUPPORT': 'Voir un évènement qui n\'a pas d\'utilisateur support',
        'WITH_DATE_START': 'Voir un évènement qui a une date de début',
        'WITHOUT_DATE_START': 'Voir un évènement qui n\'a pas de date de début',
        'WITH_DATE_STOP': 'Voir un évènement qui a une date de fin',
        'WITHOUT_DATE_STOP': 'Voir un évènement qui n\'a pas de date de fin',
    }
}
