from datetime import datetime
from enum import Enum
from typing import Any

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.text import Text

from oslui.agent import ChatAgent
from oslui.prompts import DataCell, chat_assistant_cell, RoleType
from oslui.tui import BaseTUI
from oslui.utils import get_language_type

introduction = """
# Welcome to OSLUI!

"""


class ChatTUIType(Enum):
    SINGLE = 1
    CONTINUOUS = 2


class ChatTUI(BaseTUI):
    input_msg: str = None

    def __init__(self, agent: ChatAgent, tui_type: ChatTUIType = ChatTUIType.SINGLE):
        super().__init__(agent=agent)
        self.tui_type = tui_type

    def show(self, input_msg: str = None):
        if self.tui_type == ChatTUIType.SINGLE:
            self.input_msg = input_msg
            lang_type = get_language_type(self.input_msg)
            params = {"lang_type": lang_type, "question": self.input_msg}
            self.dynamic_refresh(params)
        elif self.tui_type == ChatTUIType.CONTINUOUS:
            console = Console()
            console.clear()
            id_md = Markdown(introduction)
            console.print(id_md, style="bold green")
            try:
                while True:
                    timestamp = datetime.now().strftime("[%H:%M:%S]")
                    timestamp_text = Text(timestamp, style="bright_blue")
                    console.print(timestamp_text + " You :", style="bold bright_blue")
                    self.input_msg = console.input()

                    if not self.input_msg.strip():
                        continue
                    elif self.input_msg.lower() in ["exit", "quit", "q"]:
                        break
                    else:
                        timestamp = datetime.now().strftime("[%H:%M:%S]")
                        timestamp_text = Text(timestamp, style="green")
                        console.print(timestamp_text + " OSLUI :", style="bold green")
                        lang_type = get_language_type(self.input_msg)
                        params = {"lang_type": lang_type, "question": self.input_msg}
                        self.dynamic_refresh(params)
                        self.agent.prompt.append(chat_assistant_cell)
                        self.agent.prompt.append(DataCell(
                            role=RoleType.USER,
                            content="Question:{question}",
                            activated=False
                        ))
            except KeyboardInterrupt:
                pass

    def dynamic_refresh(self, params: dict[str, Any] = None):
        try:
            result, buffer_str = "", ""
            buffer = []
            with Live(vertical_overflow="visible") as live:
                for chunk in self.agent.run(params):
                    if "content" in chunk.choices[0]["delta"]:
                        content = chunk.choices[0]["delta"]["content"]
                        buffer_str += content
                        buffer.append(content)
                        buffer_show = "".join(buffer).strip()
                        if "\n" in content:
                            buffer = []
                            result += buffer_str
                            buffer_str = ""
                            buffer_show = ""

                        live.update(Markdown(result + f'*{buffer_show}*'))
                result += buffer_str
                live.update(Markdown(result))
        except Exception as exc:
            print(exc)
            exit(1)
