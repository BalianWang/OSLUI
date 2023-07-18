from typing import Any, List

from pydantic import BaseModel, ValidationError

from oslui.prompts import BasePrompt, DataCell, RoleType

system_cell = DataCell(
    role=RoleType.SYSTEM,
    content="You are an excellent computer expert, computer OS type is {os_type}."
            "Please generate shell commands that meet user needs"
            "##"
            "Needs:create a new git branch named develop"
            "git branch develop",
    activated=False
)

user_cell = DataCell(
    role=RoleType.USER,
    content="Needs:{lang_cmd}",
    activated=False
)

translate_cell_list = [system_cell, user_cell]


class TranslateInput(BaseModel):
    os_type: str
    lang_cmd: str


class TranslatePrompt(BasePrompt):
    params: TranslateInput = None

    def __init__(self):
        super().__init__(translate_cell_list)

    def fill_params(self, params: dict[str, Any]):
        try:
            self.params = TranslateInput(**params)
        except ValidationError as exc:
            add_info = "Parameters verification failed when completing the translate prompt"
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
