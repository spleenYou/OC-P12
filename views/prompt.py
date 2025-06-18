from rich.prompt import Prompt, Confirm
from rich.console import Console
import config.prompts as prompts
import config.config as config


class NewPrompt(Prompt):
    prompt_suffix = ' '


class Ask:
    def __init__(self, show, db, session):
        self.display = show.display
        self.session = session
        self.db = db
        self.console = Console()

    def thing(self, thing):

        self.display()
        prompt = getattr(prompts, thing)
        is_password = False
        if thing == 'department':
            departments = ' | '.join(f'{i + 1} {d}' for i, d in enumerate(self.db.get_department_list()))
            prompt = prompt.replace('departements', departments)
        if thing == 'password':
            is_password = True
            if self.session.status == 'PASSWORD_SECOND_TIME':
                prompt = prompt[:-1] + '(vérification) :'
        return NewPrompt.ask(
            '\n[dark_orange3]' + prompt + '[/dark_orange3]',
            password=is_password,
            show_default=False
        )

    def validation(self):
        """Shows a validation question

        Returns:
            bool: True by default
        """
        self.display()
        return Confirm.ask(
            f'\n[{config.validation_text_color}]{prompts.validation}[/{config.validation_text_color}]',
            default=True
        )

    def wait(self):
        "SHows a waiting line if a pause is needed"
        self.display()
        NewPrompt.ask(f'\n[{config.text_color}]{prompts.wait}[/{config.text_color}]')
