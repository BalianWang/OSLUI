from oslui.command.base import BaseCommand


class ShellCommand(BaseCommand):
    """
        ShellCommand: shell command
    """

    def __init__(self, content: str):
        super().__init__(content)
