import argparse
import os
import locale
from controllers.base import Controller
from views.prompt import Ask
from views.show import Show
from controllers.db import Mysql
from controllers.authentication import Authentication
from controllers.session import Session

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('login', nargs='?', default=None, help="Email needed as login")
    args = parser.parse_args()
    session = Session()
    app = Controller(Ask, Show, Mysql, Authentication, session)
    app.start(args.login)
    if session.status == 'LOGIN_OK':
        app.main_menu()
    os._exit(os.EX_OK)


if __name__ == "__main__":
    main()
