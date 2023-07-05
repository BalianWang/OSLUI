from oslui.command.base import BaseCommand


class LanguageCommand(BaseCommand):
    """
        LanguageCommand: language command
    """

    def __init__(self, content: str):
        super().__init__(content)
