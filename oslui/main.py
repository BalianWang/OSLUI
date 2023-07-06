import argparse
import os
import sys

from langchain.llms import OpenAI

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from oslui.prompts import TRANSLATE_PROMPT, CHAT_PROMPT
from oslui.command import LanguageCommand, ShellCommand
from oslui.agent import TranslateAgent, QueryAgent, ChatAgent


def main():
    parser = argparse.ArgumentParser(
        description="Natural Language User Interface for Operating Systems")
    parser.add_argument("language_command", help="Natural language command")
    parser.add_argument("-q", "--query", action="store_true",
                        required=False, help="Query something")
    parser.add_argument("-g", "--gpt", action="store_true",
                        required=False, help="Chat to GPT")
    args = parser.parse_args()

    llm = OpenAI(temperature=0)

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
