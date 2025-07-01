def connect_user(controller, user, monkeypatch):
    add_user(controller, user)
    controller.session.user = user
    controller.session.connected_user.email = user.email
    controller.session.set_session(filter='EMAIL')
    controller.session.connected_user = controller.db.get('USER', 0)
    controller.permissions = controller.session.connected_user.department.permissions
    controller.auth.generate_token()


def add_client(controller, client):
    controller.session.client = client
    controller.session.model = 'CLIENT'
    controller.db.add()
    controller.session.reset_session()


def add_user(controller, user):
    controller.session.user = user
    controller.session.model = 'USER'
    controller.db.add()
    controller.session.reset_session()


def add_contract(controller, contract, client_nb):
    controller.session.client = controller.db.get('CLIENT', client_nb)
    controller.session.contract = contract
    controller.session.model = 'CONTRACT'
    controller.db.add()
    controller.session.reset_session()


def add_event(controller, event, contract_nb, support_user_id, client_nb):
    controller.session.contract = controller.db.get('CONTRACT', contract_nb)
    controller.session.event = event
    event.support_contact_id = support_user_id
    controller.session.model = 'EVENT'
    controller.db.add()
    controller.session.reset_session()
