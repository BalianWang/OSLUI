import readline
import subprocess

from oslui.command.base import BaseCommand


class ShellCommand(BaseCommand):
    """
        ShellCommand: shell command
    """

    def __init__(self, content: str):
        super().__init__(content)

    def modify(self):
        readline.add_history(self.content)

        def startup_hook():
            readline.insert_text(self.content)

        readline.set_startup_hook(startup_hook)
        self.content = input()

    def run(self):
        subprocess.run(self.content, shell=True)
