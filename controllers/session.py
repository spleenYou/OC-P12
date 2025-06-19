from controllers.models import EpicUser, Client, Contract, Event


class Session:
    def __init__(self):
        self.reset_session()
        self.user = EpicUser()
        self.status = 'FIRST_LAUNCH'
        self.token = None

    def reset_session(self):
        self.new_user = EpicUser()
        self.client = Client()
        self.contract = Contract()
        self.event = Event()
        self.state = 'NORMAL'
        self.filter = ''
