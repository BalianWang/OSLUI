from abc import ABC, abstractmethod
from typing import Any


class BaseAuditor(ABC):
    """
        BaseAuditor: auditor base class
    """

    def __init__(self):
        pass

    @abstractmethod
    def audit(self, command: Any):
        pass
