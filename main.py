from controllers.session import Session
from views.show import Show


def main():
    session = Session()
    show = Show()
    user_is_logged = session.is_logged
    if not user_is_logged:
        if session.log_user():
            show.logged_ok()
            user_is_logged = True
        else:
            show.logged_nok()
    input('')


if __name__ == "__main__":
    main()
