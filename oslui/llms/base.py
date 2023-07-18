from abc import ABC, abstractmethod

from oslui.prompts import BasePrompt


class BaseLLM(ABC):
    """
        BaseLLM: large language model base class
    """

    def __init__(self, model: str, key: str = None):
        self.model = model
        self.key = key

    @abstractmethod
    def infer(self, prompt: BasePrompt):
        pass
