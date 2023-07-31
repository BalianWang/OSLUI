import platform
import subprocess
import os
import fcntl
import select
import winreg

from rich.console import Console
from rich.prompt import Prompt


def get_windows_default_shell_path():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
            value, _ = winreg.QueryValueEx(key, "!")
            return value
    except Exception as e:
        print("Error while accessing registry:", e)
        return None


def get_shell_type():
    os_type = platform.system()

    if os_type == "Windows":
        default_shell_path = get_windows_default_shell_path()
        if default_shell_path:
            if "cmd" in default_shell_path.lower():
                return "cmd"
            elif "powershell" in default_shell_path.lower():
                return "powershell"
        return "cmd"
    elif os_type == "Darwin" or os_type == "Linux":
        return os.getenv("SHELL")


def make_non_blocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)


def read_output(fd):
    output_data = b""
    while True:
        ready, _, _ = select.select([fd], [], [], 0.1)
        if not ready:
            break
        data = os.read(fd, 4096)
        if not data:
            break
        output_data += data
    return output_data.decode()


def run_command(command):
    console = Console()

    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)

    make_non_blocking(process.stdout.fileno())
    make_non_blocking(process.stderr.fileno())

    stdout_data = read_output(process.stdout.fileno())
    stderr_data = read_output(process.stderr.fileno())
    console.print(stdout_data, stderr_data, end="")

    username = os.getenv("USER") or os.getenv("USERNAME")
    current_dir = os.getcwd()

    while True:
        command = Prompt.ask(f"{username}@OSLUI:{current_dir}$ ")

        if command.lower() in ["exit", "quit", "q"]:
            break
        elif command == "clear":
            console.clear()
            continue

        process.stdin.write(command + "\n")
        process.stdin.flush()

        stdout_data = read_output(process.stdout.fileno())
        stderr_data = read_output(process.stderr.fileno())
        console.print(stdout_data, stderr_data, end="")

        if command.startwith("cd"):
            process.stdin.write("cd\n")
            process.stdin.flush()
            current_dir = read_output(process.stdout.fileno())

    process.stdin.close()
    process.wait()


if __name__ == "__main__":
    print("Welcome to the interactive Shell Terminal! Enter 'exit' to quit.")
    run_command("bash")  # 这里可以替换为其他支持的shell类型，例如"cmd"或"powershell"
