from oslui.utils import modify_string
from oslui.prompts import TRANSLATE_PROMPT
from oslui.agent import TranslateAgent, QueryAgent
from langchain.llms import OpenAI
import argparse
import os
import subprocess
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


def main():
    parser = argparse.ArgumentParser(
        description="Natural Language User Interface for Operating Systems")
    parser.add_argument("language_command", help="Natural language command")
    parser.add_argument("-q", "--query", action="store_true",
                        required=False, help="Query something")
    args = parser.parse_args()

    llm = OpenAI(temperature=0)

    if args.query:
        query_agent = QueryAgent(llm)
        result = query_agent.run(args.language_command)
        print(result)
    else:
        trans_agent = TranslateAgent(llm, TRANSLATE_PROMPT)
        command = trans_agent.run(args.language_command)
        command = modify_string(command)
        subprocess.run(command, shell=True)


if __name__ == "__main__":
    main()
