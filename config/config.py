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
env = [
    'DB_USER',
    'DB_PASSWORD',
    'DB_HOST',
    'DB_PORT',
    'DB_NAME',
    'TIME_COST',
    'MEMORY_COST',
    'PARALLELISM',
    'HASH_LEN',
    'SALT_LEN',
]
permission_table = [
    'add_user', 'update_user', 'delete_user',
    'add_client', 'update_client', 'delete_client',
    'add_contract', 'update_contract', 'delete_contract',
    'add_event', 'update_event', 'delete_event',
]
select_status = {
    'user': 'SELECT_USER',
    'support': 'SELECT_USER',
    'client': 'SELECT_CLIENT',
    'contract': 'SELECT_CONTRACT',
}
is_nullable = [
    'NOTES',
    'DATE_START',
    'DATE_STOP',
    'TOTAL_AMOUNT',
    'REST_AMOUNT',
]
is_text = [
    'COMMAND',
    'NAME',
    'PASSWORD',
    'CLIENT_NAME',
    'COMPANY_NAME',
    'LOCATION',
    'NOTES',
    'STATUS'
]
is_date = [
    'DATE_START',
    'DATE_STOP',
]
is_int = [
    'ATTENDEES',
    'EMPLOYEE_NUMBER',
    'DEPARTMENT'
]
is_float = [
    'TOTAL_AMOUNT',
    'REST_AMOUNT',
]
is_email = [
    'EMAIL',
    'CLIENT_EMAIL'
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
action_without_content = [
    'FORBIDDEN',
    'EXIT',
    'NO_CLIENT',
    'NO_CONTRACT',
    'NO_EVENT',
    'RESET',
]
authorized_action = ['HELP', 'EXIT', 'PERMISSION', 'RESET', 'FILTER']
crud_action = ['ADD', 'UPDATE', 'VIEW', 'DELETE']
app_model = ['USER', 'CLIENT', 'CONTRACT', 'EVENT']
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
        'SIGNED': 'Voir un contrat qui est signé',
        'UNSIGNED': 'Voir un contrat qui n\'est pas signé',
        'PAID': 'Voir un contrat qui est payé',
        'UNPAID': 'Voir un contrat qui n\'est pas payé',
        'PARTIAL_PAID': 'Voir un contrat qui est partiellement payé',
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
col = {
    'session': ['', '', '', ''],
    'select_user': ['N°', 'N° d\'employé', 'Nom', 'Email', 'Département'],
    'select_client': ['N°', 'Nom de l\'entreprise', 'Contact'],
    'select_contract': ['N°', 'Date de création', 'Montant total', 'Status'],
    'permissions': ['Command', 'commercial', 'support', 'management'],
    'help': ['', '', '', '', ''],
    'filter': ['', ''],
    'model': ['', ''],
    'user': ['', ''],
    'client': ['', ''],
    'contract': ['', ''],
    'event': ['', ''],
    'users': ['N° d\'employé', 'Nom', 'Département', 'Adresse mail', 'Date de création'],
    'clients': ['Entreprise', 'Contact', 'Adresse mail', 'Téléphone', 'Dernière mise à jour', 'Création'],
    'contracts': ['Client', 'Montant total', 'Restant à payer', 'Status', 'Création'],
    'events': ['Client', 'Montant total', 'Lieu', 'Nb de personnes', 'Début', 'Fin', 'Création'],
}
text_help = ('Syntaxe : ACTION CATEGORIE *\n\n'
             '* Pour voir les filtres disponibles taper FILTER\n\n'
             'L\'accès à certaines actions est restreint en fonction des permissions'
             ' attribuées à votre département\n\n'
             'Pour les connaître taper PERMISSION\n\n'
             'RESET PASSWORD pour redéfinir votre mot de passe')
filter_text = ('Syntaxe: COMMAND FILTER\n\n'
               'Permet d\'afficher les détails d\'un élément parmi une liste\n\n'
               'Syntaxe: COMMAND ALL FILTER\n\n'
               'Permet d\'afficher un tableau avec tous les éléments du filtre\n\n')
