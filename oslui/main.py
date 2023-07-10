import argparse
import logging
import os
import sys

from langchain.llms import OpenAI

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from oslui.utils import get_environment_variable
from oslui.agent import TranslateAgent, QueryAgent, ChatAgent
from oslui.command import LanguageCommand, ShellCommand
from oslui.prompts import TRANSLATE_PROMPT, CHAT_PROMPT


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

    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

    if args.gpt:
        chat_agent = ChatAgent(llm, CHAT_PROMPT)
        result = chat_agent.run(args.language_command)
        print(result)
    elif args.query:
        query_agent = QueryAgent(llm)
        result = query_agent.run(args.language_command)
        print(result)
    else:
        trans_agent = TranslateAgent(llm, TRANSLATE_PROMPT)
        lang_cmd = LanguageCommand(args.language_command)
        sh_cmd = ShellCommand(trans_agent.run(lang_cmd.content))
        sh_cmd.modify()
        sh_cmd.run()


if __name__ == "__main__":
    main()
