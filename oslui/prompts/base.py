from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, List


class RoleType(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"


class DataCell(object):
    def __init__(self, role: RoleType, content: str, max_tokens: int = None, temperature: float = 0,
                 activated: bool = True, stream: bool = False):
        self.role = role
        self.content = content
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.activated = activated
        self.stream = stream

    def __dict__(self):
        if not self.activated:
            raise Exception("DataCell not activated")
        return {'role': self.role.value, 'content': self.content}

    def activate(self, params: dict[str, Any]):
        if not self.activated:
            self.content = self.content.format(**params)
            self.activated = True


class BasePrompt(ABC):
    """
        BasePrompt: prompt base class
    """

    cell_list: List[DataCell] = None
    ready: bool = False
    temperature: float = 0
    max_tokens: int = None
    stream: bool = False

    def __init__(self, cell_list: List[DataCell]):
        self.cell_list = cell_list

    @abstractmethod
    def fill_params(self, params: dict[str, Any]):
        pass

    @abstractmethod
    def append(self, cell: DataCell):
        pass

    @abstractmethod
    def prompt(self) -> List[dict[str, str]]:
        pass
