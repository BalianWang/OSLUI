from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """
        BaseCommand: command base class
    """

    def __init__(self, content: str):
        self.content = content
