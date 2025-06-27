def connect_user(controller, user, monkeypatch):
    controller.session.user = user
    controller.db.add('user')
    controller.session.reset_session()
    controller.session.connected_user = controller.db.get_user_by_mail(user.email)
    controller.permissions = controller.session.connected_user.department.permissions
    controller.auth.generate_token()


def add_client(controller, client):
    controller.session.client = client
    controller.db.add('client')
    controller.session.reset_session()


def add_user(controller, user):
    controller.session.user = user
    controller.db.add('user')
    controller.session.reset_session()


def add_contract(controller, contract, client_nb):
    controller.session.client = controller.db.get_client(client_nb)
    controller.session.contract = contract
    controller.db.add('contract')
    controller.session.reset_session()


def add_event(controller, event, contract_nb, support_user_id, client_nb):
    event.support_contact_id = support_user_id
    controller.session.status = 'SELECT_CONTRACT_WITHOUT_EVENT'
    controller.session.client = controller.db.get_client(client_nb)
    controller.session.contract = controller.db.get_contract(contract_nb)
    controller.session.event = event
    controller.db.add('event')
    controller.session.reset_session()
