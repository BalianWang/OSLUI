from abc import ABC, abstractmethod

from oslui.agent import BaseAgent


class BaseTUI(ABC):
    """
        BaseTUI: terminal user interface base class
    """

    def __init__(self, agent: BaseAgent):
        self.agent = agent

    @abstractmethod
    def show(self, input_msg: str = None):
        pass
