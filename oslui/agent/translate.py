from typing import Any

from guidance.llms import LLM
from pydantic import ValidationError

from oslui.agent.base import BaseAgent
from oslui.prompts import TRANSLATE_PROMPT, TranslateInput, TranslateOutput


class TranslateAgent(BaseAgent):
    """
        TranslateAgent: translate natural language command to shell command
    """
    params: TranslateInput = None
    result: TranslateOutput = None

    def __init__(self, llm: LLM):
        super().__init__(llm=llm, prompt=TRANSLATE_PROMPT)

    def run(self, params_dict: dict[str, Any]):
        try:
            self.params = TranslateInput(**params_dict)
        except ValidationError as exc:
            add_info = "Parameters verification failed before generating shell commands"
            new_exc = Exception(f"Error occurred: {add_info}")
            new_exc.__cause__ = exc
            raise new_exc

        output_dict = {}
        try:
            output = self.program(os_type=self.params.os_type, needs=self.params.needs)
            output_dict["shell_cmd"] = output["shell_cmd"]
        except Exception as exc:
            add_info = "Something wrong when generating shell commands"
            new_exc = Exception(f"Error occurred: {add_info}")
            new_exc.__cause__ = exc
            raise new_exc

        try:
            self.result = TranslateOutput(**output_dict)
        except ValidationError as exc:
            add_info = "Generated shell commands are not as expected"
            new_exc = Exception(f"Error occurred: {add_info}")
            new_exc.__cause__ = exc
            raise new_exc
