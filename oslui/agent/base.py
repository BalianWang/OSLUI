from abc import ABC, abstractmethod
from typing import Any

from oslui.llms import BaseLLM
from oslui.prompts import BasePrompt


class BaseAgent(ABC):
    """
        BaseAgent: OS Agent base class
    """

    def __init__(self, llm: BaseLLM, prompt: BasePrompt):
        self.llm = llm
        self.prompt = prompt

    @abstractmethod
    def run(self, params: dict[str, Any] = None):
        pass
