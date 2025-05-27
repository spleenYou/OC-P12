from controllers.base import Controller
from views.prompt import Prompt
from views.show import Show
from controllers.mysql import Mysql


def main():
    app = Controller(Prompt, Show, Mysql)
    app.first_launch()
    if app.user_is_logged():
        print('ok')
    else:
        print('nok')
    input('')


if __name__ == "__main__":
    main()
