from typing import Any, List

from pydantic import BaseModel, ValidationError

from oslui.prompts import BasePrompt, DataCell, RoleType

chat_system_cell = DataCell(
    role=RoleType.SYSTEM,
    content="You are a helpful assistant, and you are the best expert to answer user's question."
            "It is recommended to use markdown syntax when necessary."
            "Please use {lang_type} answer questions as detail as possible.",
    activated=False
)

chat_user_cell = DataCell(
    role=RoleType.USER,
    content="Question:{question}",
    activated=False
)

chat_assistant_cell = DataCell(
    role=RoleType.ASSISTANT,
    content="Detailed answer to the previous question"
)

chat_cell_list = [chat_system_cell, chat_user_cell]


class ChatInput(BaseModel):
    question: str
    lang_type: str


class ChatPrompt(BasePrompt):
    params: ChatInput = None

    def __init__(self):
        super().__init__(chat_cell_list)
        self.stream = True

    def fill_params(self, params: dict[str, Any]):
        try:
            self.params = ChatInput(**params)
        except ValidationError as exc:
            add_info = "Parameters verification failed when completing the chat prompt"
            new_exc = Exception(f"Error occurred: {add_info}")
            new_exc.__cause__ = exc
            raise new_exc

        for cell in self.cell_list:
            cell.activate(params)

        self.ready = True

    def append(self, cell: DataCell):
        self.cell_list.append(cell)
        if cell.temperature != 0:
            self.temperature = cell.temperature
        if cell.max_tokens:
            self.max_tokens = cell.max_tokens

    def prompt(self) -> List[dict[str, str]]:
        return [cell.__dict__() for cell in self.cell_list]
