from typing import Any, List

from pydantic import BaseModel, ValidationError

from oslui.prompts import BasePrompt, DataCell, RoleType

debug_system_cell = DataCell(
    role=RoleType.SYSTEM,
    content="You are a helpful assistant, and you are are the best computer expert in the world."
            "An error occurred when the user executed shell command on the computer."
            "Please give the best solution or suggestion based on the error message."
            "It is recommended to use markdown syntax when necessary.",
    activated=False
)

debug_user_cell = DataCell(
    role=RoleType.USER,
    content="Shell command: {command},"
            "Error message: {error_msg},"
            "OS: {os_type}",
    activated=False
)

debug_cell_list = [debug_system_cell, debug_user_cell]


class DebugInput(BaseModel):
    command: str
    error_msg: str
    os_type: str


class DebugPrompt(BasePrompt):
    params: DebugInput = None

    def __init__(self):
        super().__init__(debug_cell_list)
        self.stream = True

    def fill_params(self, params: dict[str, Any]):
        try:
            self.params = DebugInput(**params)
        except ValidationError as exc:
            add_info = "Parameters verification failed when completing the debug prompt"
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
