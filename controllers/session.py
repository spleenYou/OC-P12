class Session:
    def __init__(self):
        self.user = {
            'id': None,
            'name': None,
            'email': None,
            'password': None,
            'employee_number': None,
            'department_id': None
        }
        self.reset_new_user()
        self.reset_client()
        self.contract = {
            'id': None,
            'client_id': None,
            'total_amount': None,
            'rest_amount': None,
            'status': None
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
        self.status = None
        self.token = None

    def reset_new_user(self):
        self.new_user = {
            'id': None,
            'name': None,
            'email': None,
            'password': None,
            'employee_number': None,
            'department_id': None
        }

    def reset_client(self):
        self.client = {
            'id': None,
            'name': None,
            'email': None,
            'phone': None,
            'company_name': None,
            'commercial_contact_id': None
        }
