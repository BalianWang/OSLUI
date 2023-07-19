import openai

from oslui.llms.base import BaseLLM
from oslui.prompts import BasePrompt
from oslui.utils import get_environment_variable


class OpenAI(BaseLLM):
    def __init__(self, model: str, key: str = None):
        if not key:
            key = get_environment_variable("OPENAI_API_KEY")
        super().__init__(model=model, key=key)

    def infer(self, prompt: BasePrompt) -> str:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=prompt.prompt(),
            temperature=prompt.temperature,
            max_tokens=prompt.max_tokens,
            stream=prompt.stream,
        )

        return response
