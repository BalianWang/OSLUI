import os
import subprocess

from prompt_toolkit import prompt


def get_prompt():
    # 获取用户名和主机名
    username = os.getenv("USER") or os.getenv("USERNAME")
    machine = os.uname().nodename

    # 获取当前工作目录
    current_dir = os.getcwd()

    # 构造提示信息
    return f"{username}@{machine}: {current_dir} $ "


def run_command(command):
    # 创建一个子进程
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)

    # 循环执行交互命令
    while True:
        # 读取用户输入的命令
        user_input = prompt(get_prompt())

        # 如果用户输入 'exit'，则退出循环
        if user_input.lower() == 'exit':
            break

        # 检查是否输入了 cd 命令
        if user_input.startswith("cd "):
            new_directory = user_input[3:].strip()
            try:
                # 改变当前目录
                os.chdir(new_directory)
            except FileNotFoundError:
                print("Directory not found.")
            continue

        # 将命令写入子进程的stdin
        process.stdin.write(user_input + "\n")
        process.stdin.flush()

        # 读取并显示命令执行结果
        stdout, stderr = process.communicate()
        print(stdout, end="")
        print(stderr, end="")

    # 关闭子进程
    process.stdin.close()
    process.wait()


if __name__ == "__main__":
    print("Welcome to the interactive Shell Terminal! Enter 'exit' to quit.")
    run_command("bash")  # 这里可以替换为其他支持的shell类型，例如"cmd"或"powershell"
