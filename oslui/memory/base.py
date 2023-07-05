from abc import ABC, abstractmethod
from enum import Enum
from typing import Union

from langchain.memory import ChatMessageHistory


class MemoryDataType(Enum):
    UNKNOWN = 1
    DIALOG = 2
    STRING = 3


class MemorySourceType(Enum):
    UNKNOWN = 1
    LOCAL_FILE = 2
    LOCAL_DB = 3
    REMOTE_FILE = 4
    REMOTE_DB = 5


class BaseMemorySource(ABC):
    """
        BaseMemorySource: memory source base class
    """

    def __init__(self, source_type: MemorySourceType, src: str):
        self.source_type = source_type
        self.src = src

    @abstractmethod
    def read(self) -> bytes:
        pass

    @abstractmethod
    def write(self, data: bytes):
        pass


class BaseMemoryData(ABC):
    """
        BaseMemoryData: memory data base class
    """

    def __init__(self, date_type: MemorySourceType, data: Union[str, ChatMessageHistory]):
        self.date_type = date_type
        self.data = data


class BaseMemory(ABC):
    """
        BaseMemory: memory base class
    """

    def __init__(self, data: BaseMemoryData, source: BaseMemorySource):
        self.data = data
        self.source = source

    @abstractmethod
    def recall(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def clear(self):
        pass
