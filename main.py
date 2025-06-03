import argparse
from controllers.base import Controller
from views.prompt import Prompt
from views.show import Show
from controllers.mysql import Mysql
from controllers.authentication import Authentication
from controllers.models import EpicUser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('login', nargs='?', default=None, help="Email needed as login")
    args = parser.parse_args()
    app = Controller(Prompt, Show, Mysql, Authentication)
    user = EpicUser()
    user.email = args.login
    app.start(user)


if __name__ == "__main__":
    main()
