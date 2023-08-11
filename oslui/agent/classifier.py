from enum import Enum
from typing import Any

from oslui.agent import BaseAgent
from oslui.llms import BaseLLM
from oslui.prompts import ClassifierPrompt


class IntentType(Enum):
    UNKNOWN = 0
    SHELL = 1
    PROGRAM = 2
    IN_QUERY = 3
    OUT_QUERY = 4


class ClassifierAgent(BaseAgent):
    """
        ClassifierAgent: identify user intent
    """

    def __init__(self, llm: BaseLLM):
        super().__init__(llm=llm, prompt=ClassifierPrompt())

    def run(self, params: dict[str, Any] = None):
        try:
            self.prompt.fill_params(params)
        except Exception as exc:
            add_info = "Parameters complete failed before identifying user intent"
            new_exc = Exception(f"Error occurred: {add_info}")
            new_exc.__cause__ = exc
            raise new_exc

        try:
            response = self.llm.infer(self.prompt)
            result = response["choices"][0]["message"]["content"]
        except Exception as exc:
            print(exc)
            add_info = "Something wrong when identifying user intent"
            new_exc = Exception(f"Error occurred: {add_info}")
            new_exc.__cause__ = exc
            raise new_exc

        if result == "1":
            return IntentType.SHELL
        elif result == "2":
            return IntentType.PROGRAM
        elif result == "3":
            return IntentType.IN_QUERY
        elif result == "4":
            return IntentType.OUT_QUERY

        return IntentType.UNKNOWN
