from pydantic import BaseModel

TRANSLATE_PROMPT = \
    """
    {{#system~}}
    You are an excellent computer expert assistant.
    {{~/system}}

    {{! generate shell commands that meet user needs}}
    {{#user~}}
    My computer OS type is {{os_type}}, my needs are {{needs}}
    {{~/user}}

    {{#assistant~}}
    {{gen 'shell_cmd' temperature=0}}
    {{~/assistant}}
    """


class TranslateInput(BaseModel):
    os_type: str
    needs: str


class TranslateOutput(BaseModel):
    shell_cmd: str
