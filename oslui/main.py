import argparse
import logging
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from oslui.tui import ChatTUIType, ChatTUI, DebugTUI
from oslui.llms import OpenAI
from oslui.action import ShellCommand
from oslui.agent import TranslateAgent, ChatAgent, ClassifierAgent, IntentType, DebugAgent
from oslui.utils import get_environment_variable, get_os_type


def main():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    logging.getLogger('').addHandler(console_handler)

    parser = argparse.ArgumentParser(
        description="Natural Language User Interface for Operating Systems")
    parser.add_argument('lang_cmd', type=str, nargs='*',
                        help="Natural language command")
    parser.add_argument("-i", "--immerse", action="store_true",
                        required=False, help="Immerse mode")
    parser.add_argument("-d", "--debug", action="store_true",
                        required=False, help="Debug for your confusing questions")

    args = parser.parse_args()

    try:
        openai_api_key = get_environment_variable("OPENAI_API_KEY")
    except Exception as e:
        logging.error(str(e))
        exit(1)

    llm = OpenAI(model="gpt-3.5-turbo", key=openai_api_key)

    selected_count = sum([1 for arg in [args.immerse, args.debug] if arg])
    if selected_count > 1:
        parser.error(
            "Parameter conflict: only one of -i or -d can be selected")

    if args.immerse:
        chat_agent = ChatAgent(llm)
        tui = ChatTUI(chat_agent, tui_type=ChatTUIType.CONTINUOUS)
        tui.show()
    elif args.debug:
        debug_agent = DebugAgent(llm)
        tui = DebugTUI(debug_agent)
        tui.show()
    else:
        lang_cmd = ' '.join(args.lang_cmd)
        classifier = ClassifierAgent(llm)
        try:
            params = {"sentence": lang_cmd}
            intent = classifier.run(params)
        except Exception as exc:
            print(exc)
            exit(1)

        if intent == IntentType.SHELL or intent == IntentType.PROGRAM:
            trans_agent = TranslateAgent(llm)
            try:
                os_type = get_os_type()
                params = {"os_type": os_type, "lang_cmd": lang_cmd}
                result = trans_agent.run(params)
            except Exception as exc:
                print(exc)
                exit(1)

            sh_cmd = ShellCommand(result)
            sh_cmd.modify()
            sh_cmd.execute()
        elif intent == IntentType.IN_QUERY or intent == IntentType.OUT_QUERY:
            chat_agent = ChatAgent(llm)
            tui = ChatTUI(chat_agent)
            tui.show(lang_cmd)


if __name__ == "__main__":
    main()
