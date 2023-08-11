from typing import Any

from oslui.agent import BaseAgent
from oslui.llms import BaseLLM
from oslui.prompts import TranslatePrompt


class TranslateAgent(BaseAgent):
    """
        TranslateAgent: translate natural language command to shell command
    """

    def __init__(self, llm: BaseLLM):
        super().__init__(llm=llm, prompt=TranslatePrompt())

    def run(self, params: dict[str, Any] = None) -> str:
        try:
            self.prompt.fill_params(params)
        except Exception as exc:
            add_info = "Parameters complete failed before generating shell commands"
            new_exc = Exception(f"Error occurred: {add_info}")
            new_exc.__cause__ = exc
            raise new_exc

        try:
            response = self.llm.infer(self.prompt)
            result = response["choices"][0]["message"]["content"]
        except Exception as exc:
            add_info = "Something wrong when generating shell commands"
            new_exc = Exception(f"Error occurred: {add_info}")
            new_exc.__cause__ = exc
            raise new_exc

        return result
