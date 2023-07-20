import argparse
import logging
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from oslui.utils import get_environment_variable, get_os_type
from oslui.agent import TranslateAgent, ChatAgent
from oslui.action import ShellCommand
from oslui.llms import OpenAI
from oslui.tui import ChatTUIType, ChatTUI


def main():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    logging.getLogger('').addHandler(console_handler)

    parser = argparse.ArgumentParser(
        description="Natural Language User Interface for Operating Systems")
    parser.add_argument("lang_cmd", nargs="?", default=None, help="Natural language command")
    parser.add_argument("-c", "--chat", action="store_true",
                        required=False, help="Chat, communicate or consult something")

    args = parser.parse_args()

    try:
        openai_api_key = get_environment_variable("OPENAI_API_KEY")
    except Exception as e:
        logging.error(str(e))
        exit(1)

    llm = OpenAI(model="gpt-3.5-turbo", key=openai_api_key)

    if args.chat:
        chat_agent = ChatAgent(llm)
        tui = ChatTUI(chat_agent)
        tui.show(args.lang_cmd)
    else:
        if args.lang_cmd:
            trans_agent = TranslateAgent(llm)
            try:
                os_type = get_os_type()
                params = {"os_type": os_type, "lang_cmd": args.lang_cmd}
                result = trans_agent.run(params)
            except Exception as exc:
                print(exc)
                exit(1)

            sh_cmd = ShellCommand(result)
            sh_cmd.modify()
            sh_cmd.execute()
        else:
            chat_agent = ChatAgent(llm)
            tui = ChatTUI(chat_agent, tui_type=ChatTUIType.CONTINUOUS)
            tui.show()


if __name__ == "__main__":
    main()
