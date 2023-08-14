import os
import subprocess

from typing import Any

from oslui.agent import BaseAgent
from oslui.llms import BaseLLM
from oslui.prompts import DebugPrompt
from oslui.utils import get_os_type


class DebugAgent(BaseAgent):
    """
        DebugAgent: debug agent
    """
    command: str = ""
    error_msg: str = ""
    os_type: str = ""
    params: dict[str, Any] = {}

    def __init__(self, llm: BaseLLM):
        super().__init__(llm=llm, prompt=DebugPrompt())

    def get_command(self):
        tty_name = os.ttyname(0)
        tty_id = os.path.basename(tty_name)
        command_log = os.path.expanduser(f"~/.oslui/command_log/{tty_id}.log")
        try:
            with open(command_log, 'r') as file:
                lines = file.readlines()
                if lines:
                    command_line = -1
                    while True:
                        command = lines[command_line].strip()
                        if command == "oslui -d":
                            command_line -= 1
                            continue
                        else:
                            self.command = command
                            break
        except FileNotFoundError:
            pass

    def get_error_msg(self):
        try:
            result = subprocess.run(
                self.command, shell=True, check=True, text=True, capture_output=True)

            # command executed unsuccessfully
            if result.returncode != 0:
                self.error_msg = result.stderr

        except subprocess.CalledProcessError as e:
            self.error_msg = e.stderr

    def get_os_type(self):
        self.os_type = get_os_type()

    def get_params(self):
        self.get_command()
        if self.command == "":
            exc = Exception("Could not get command")
            raise exc
        self.get_error_msg()
        if self.error_msg == "":
            exc = Exception("Could not get error message")
            raise exc
        self.get_os_type()
        if self.os_type == "":
            exc = Exception("Could not get os type")
            raise exc
        self.params["command"] = self.command
        self.params["error_msg"] = self.error_msg.replace(
            '"', "'").replace('\n', ' ')
        self.params["os_type"] = self.os_type

    def run(self, params: dict[str, Any] = None):
        self.get_params()
        try:
            self.prompt.fill_params(self.params)
        except Exception as exc:
            add_info = "Parameters complete failed before debugging"
            new_exc = Exception(f"Error occurred: {add_info}")
            new_exc.__cause__ = exc
            raise new_exc

        try:
            response = self.llm.infer(self.prompt)
        except Exception as exc:
            add_info = "Something wrong when debugging"
            new_exc = Exception(f"Error occurred: {add_info}")
            new_exc.__cause__ = exc
            raise new_exc

        return response
