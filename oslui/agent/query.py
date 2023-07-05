from typing import List

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.agents.agent import AgentExecutor
from langchain.llms.base import BaseLLM
from langchain.prompts import PromptTemplate
from langchain.tools.base import BaseTool

from oslui.agent.base import BaseAgent


class QueryAgent(BaseAgent):
    """
        QueryAgent: support query something in terminal
    """
    tools: List[BaseTool] = None
    agent: AgentExecutor = None

    def __init__(self, llm: BaseLLM, prompt: PromptTemplate = None, memory: PromptTemplate = None,
                 tools: List[str] = None):
        super().__init__(llm, prompt, memory)
        if tools:
            self.tools = load_tools(tools, llm=llm)
        else:
            self.tools = load_tools(["serpapi"], llm=llm)
        self.agent = initialize_agent(
            self.tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)

    def run(self, input_msg: str) -> str:
        return self.agent.run(input_msg)
