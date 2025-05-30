from controllers.base import Controller
from views.prompt import Prompt
from views.show import Show
from controllers.mysql import Mysql
from controllers.authentication import Authentication


def main():
    app = Controller(Prompt, Show, Mysql, Authentication)
    app.first_launch()
    if app.user_is_logged():
        print('ok')
    else:
        print('nok')


if __name__ == "__main__":
    main()
