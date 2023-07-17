from pydantic import BaseModel

CHAT_PROMPT = \
    """
    {{#system~}}
    You are a helpful assistant.
    {{~/system}}
    
    {{#user~}}
    I want a response to the following question:
    {{query}}
    Name 3 world-class experts (past or present) who would be great at answering this?
    Don't answer the question yet.
    {{~/user}}
    
    {{#assistant~}}
    {{gen 'expert_names' temperature=0 max_tokens=300}}
    {{~/assistant}}
    
    {{#user~}}
    Great, now please answer the question as if these experts had collaborated in writing a joint anonymous answer.
    Please use {{language_type}} as detailed as possible.
    {{~/user}}
    
    {{#assistant~}}
    {{gen 'answer' temperature=0}}
    {{~/assistant}}
    """


class ChatInput(BaseModel):
    query: str
    language_type: str


class ChatOutput(BaseModel):
    answer: str
