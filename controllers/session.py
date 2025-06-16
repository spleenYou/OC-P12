class Session:
    def __init__(self):
        self.reset_session()
        self.user = {
            'id': None,
            'name': None,
            'email': None,
            'password': None,
            'employee_number': None,
            'department_id': None
        }
        self.status = 'FIRST_LAUNCH'
        self.token = None

    def reset_session(self):
        self.new_user = {
            'id': None,
            'name': None,
            'email': None,
            'password': None,
            'employee_number': None,
            'department_id': None
        }
        self.client = {
            'id': None,
            'name': None,
            'email': None,
            'phone': None,
            'company_name': None,
            'commercial_contact_id': None
        }
        self.contract = {
            'id': None,
            'client_id': None,
            'total_amount': None,
            'rest_amount': None,
            'status': False
        }
        self.event = {
            'id': None,
            'support_contact_id': None,
            'location': None,
            'attendees': None,
            'notes': None,
            'date_start': None,
            'date_stop': None
        }
