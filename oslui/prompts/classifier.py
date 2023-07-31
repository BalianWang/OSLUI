from typing import Any, List

from pydantic import BaseModel, ValidationError

from oslui.prompts import BasePrompt, DataCell, RoleType

classifier_system_cell = DataCell(
    role=RoleType.SYSTEM,
    content="Please identify which of the following intent the given sentence belongs to."
            "And reply the sequence number before the corresponding intent."
            "1 Execute shell commands on the computer"
            "2 Asking a question that you are sure you can answer"
            "3 Asking a question that you need external toos or data to answer"
            "4 A large task needs tp be split and completed step by step"
            "5 Others"
            "##"
            "Sentence:create a new git branch named develop"
            "1"
            "##"
            "Sentence:the latest versions and features of Python"
            "3",
    activated=False
)

classifier_user_cell = DataCell(
    role=RoleType.USER,
    content="Sentence:{sentence}",
    activated=False
)

classifier_cell_list = [classifier_system_cell, classifier_user_cell]


class ClassifierInput(BaseModel):
    sentence: str


class ClassifierPrompt(BasePrompt):
    params: ClassifierInput = None

    def __init__(self):
        super().__init__(classifier_cell_list)

    def fill_params(self, params: dict[str, Any]):
        try:
            self.params = ClassifierInput(**params)
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
