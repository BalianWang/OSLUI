import readline


def modify_string(input_string: str) -> str:
    readline.add_history(input_string)

    def startup_hook():
        readline.insert_text(input_string)

    readline.set_startup_hook(startup_hook)
    edited_input = input()

    return edited_input
