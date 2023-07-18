import argparse
import logging
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from oslui.utils import get_environment_variable, get_os_type
from oslui.agent import TranslateAgent
from oslui.command import LanguageCommand
from oslui.llms import OpenAI


def main():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    logging.getLogger('').addHandler(console_handler)

    parser = argparse.ArgumentParser(
        description="Natural Language User Interface for Operating Systems")
    parser.add_argument("language_command", help="Natural language command")
    parser.add_argument("-q", "--query", action="store_true",
                        required=False, help="Query something")
    parser.add_argument("-g", "--gpt", action="store_true",
                        required=False, help="Chat to GPT")

    args = parser.parse_args()

    try:
        openai_api_key = get_environment_variable("OPENAI_API_KEY")
    except Exception as e:
        logging.error(str(e))
        exit(1)

    llm = OpenAI(model="gpt-3.5-turbo", key=openai_api_key)

    if args.gpt:
        """
        chat_agent = ChatAgent(llm)
        try:
            language_type = get_language_type(args.language_command)
            params = {"language_type": language_type, "query": args.language_command}
            chat_agent.run(params)
        except Exception as exc:
            print(exc)
            exit(1)
        print(chat_agent.result.answer)
        """
    elif args.query:
        pass
    else:
        trans_agent = TranslateAgent(llm)
        lang_cmd = LanguageCommand(args.language_command)
        try:
            os_type = get_os_type()
            params = {"os_type": os_type, "lang_cmd": lang_cmd.content}
            print(trans_agent.run(params))
        except Exception as exc:
            print(exc)
            exit(1)

        """
        sh_cmd = ShellCommand(trans_agent.result.shell_cmd)
        sh_cmd.modify()
        sh_cmd.run()
        """


if __name__ == "__main__":
    main()
