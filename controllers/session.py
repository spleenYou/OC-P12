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
        self.status = None
        self.new_user = {
            'id': None,
            'name': None,
            'email': None,
            'password': None,
            'employee_number': None,
            'department_id': None
        }
        self.client = {
            'name': None,
            'email': None,
            'phone': None,
            'company_name': None,
            'commercial_contact_id': None
        }
        self.token = None
        self.first_launch = True
