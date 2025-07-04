import argparse
import locale
from controllers.base import Controller
from views.prompt import Ask
from views.show import Show
from controllers.db import Mysql
from controllers.authentication import Authentication
from controllers.session import Session
import sentry_sdk

"Set date in french"
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

sentry_sdk.init(
    dsn="https://658b44973063f1d61a14d521cf60ae2d@o4509252956127232.ingest.de.sentry.io/4509546953375824",
    send_default_pii=True,
)


def main():
    "Retrieve the email argument (if given) before launching the application"
    parser = argparse.ArgumentParser()
    parser.add_argument('login', nargs='?', default=None, help="Email needed as login")
    args = parser.parse_args()
    app = Controller(Ask, Show, Mysql, Authentication, Session)
    app.start(args.login)


if __name__ == "__main__":
    main()
