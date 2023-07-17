from typing import Any

from guidance.llms import LLM
from pydantic import ValidationError

from oslui.agent.base import BaseAgent
from oslui.prompts import ChatOutput, ChatInput, CHAT_PROMPT


class ChatAgent(BaseAgent):
    """
        TranslateAgent: translate natural language command to shell command
    """
    params: ChatInput = None
    result: ChatOutput = None

    def __init__(self, llm: LLM):
        super().__init__(llm=llm, prompt=CHAT_PROMPT)

    def run(self, params_dict: dict[str, Any]):
        try:
            self.params = ChatInput(**params_dict)
        except ValidationError as exc:
            add_info = "Parameters verification failed before generating chat answer"
            new_exc = Exception(f"Error occurred: {add_info}")
            new_exc.__cause__ = exc
            raise new_exc

        output_dict = {}
        try:
            output = self.program(language_type=self.params.language_type, query=self.params.query)
            output_dict["answer"] = output["answer"]
        except Exception as exc:
            add_info = "Something wrong when generating chat answer"
            new_exc = Exception(f"Error occurred: {add_info}")
            new_exc.__cause__ = exc
            raise new_exc

        try:
            self.result = ChatOutput(**output_dict)
        except ValidationError as exc:
            add_info = "Generated chat answer are not as expected"
            new_exc = Exception(f"Error occurred: {add_info}")
            new_exc.__cause__ = exc
            raise new_exc
