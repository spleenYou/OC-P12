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
    'email',
    'password',
    'client_name',
    'phone',
    'company_name',
    'location',
    'notes'

]
is_date = [
    'date_start',
    'date_stop',
]
is_int = [
    'attendees',
    'employee_number',
]
is_float = [
    'total_amount',
    'rest_amount',
]
is_email = [
    'email',
    'client_email'
]
is_phone = [
    'phone'
]
