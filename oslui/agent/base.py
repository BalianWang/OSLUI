from abc import ABC, abstractmethod

from langchain.llms.base import BaseLLM
from langchain.prompts import PromptTemplate


class BaseAgent(ABC):
    """
        BaseAgent: OS Agent base class
    """

    def __init__(self, llm: BaseLLM, prompt: PromptTemplate = None, memory: PromptTemplate = None):
        self.llm = llm
        self.prompt = prompt
        self.memory = memory

    @abstractmethod
    def run(self, input_msg: str) -> str:
        pass
