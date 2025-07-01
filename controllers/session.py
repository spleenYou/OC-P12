from controllers.models import EpicUser, Client, Contract, Event


class Session:
    def __init__(self):
        self.reset_session()
        self.connected_user = EpicUser()
        self.token = None

    def reset_session(self):
        self.user = EpicUser()
        self.client = Client()
        self.contract = Contract()
        self.event = Event()
        self.state = 'NORMAL'
        self.filter = ''
        self.model = ''
        self.want_all = False
        self.user_cmd = ''
        self.action = ''

    def set_session(
            self,
            action=None,
            model=None,
            state=None,
            filter=None,
            want_all=None,
            user_cmd=None):
        if action is not None:
            self.action = action
        if model is not None:
            self.model = model
        if state is not None:
            self.state = state
        if filter is not None:
            self.filter = filter
        if want_all is not None:
            self.want_all = want_all
        if user_cmd is not None:
            self.user_cmd = user_cmd
