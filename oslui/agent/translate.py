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

    def run(self, params: dict[str, Any]):
        try:
            self.prompt.fill_params(params)
        except Exception as exc:
            add_info = "Parameters complete failed before generating shell commands"
            new_exc = Exception(f"Error occurred: {add_info}")
            new_exc.__cause__ = exc
            raise new_exc

        result = self.llm.infer(self.prompt)
        print(result)
