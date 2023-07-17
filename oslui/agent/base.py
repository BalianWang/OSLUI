from abc import ABC, abstractmethod
from typing import Any

import guidance
from guidance.llms import LLM


class BaseAgent(ABC):
    """
        BaseAgent: OS Agent base class
    """

    def __init__(self, llm: LLM, prompt: str = None):
        self.llm = llm
        self.prompt = prompt
        self.program = guidance(template=prompt, llm=llm)

    @abstractmethod
    def run(self, params: dict[str, Any]):
        pass
