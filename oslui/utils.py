import os
import platform
import re


def get_environment_variable(variable_name):
    try:
        value = os.environ[variable_name]
        return value
    except KeyError:
        raise Exception(f"environment variable {variable_name} does not exist")


def get_os_type() -> str:
    os_type = "Linux"
    os_name = platform.system()
    if os_name == "Windows":
        os_type = "Windows"
    elif os_name == "Darwin":
        os_type = "Mac"
    elif os_name == "Linux":
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME"):
                        _, distribution = line.strip().split("=", 1)
                        os_type = distribution.strip('"')
        except FileNotFoundError:
            pass

    return os_type


def get_language_type(text) -> str:
    text = re.sub(r"[^\w\s]", "", text)

    if any("\u4e00" <= c <= "\u9fff" for c in text):
        return "Chinese"
    else:
        return "English"
