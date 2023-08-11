from rich.live import Live
from rich.markdown import Markdown

from oslui.agent import DebugAgent
from oslui.tui import BaseTUI


class DebugTUI(BaseTUI):
    def __init__(self, agent: DebugAgent):
        super().__init__(agent=agent)

    def show(self, input_msg: str = None):
        self.dynamic_refresh()

    def dynamic_refresh(self):
        try:
            result, buffer_str = "", ""
            buffer = []
            with Live(vertical_overflow="visible") as live:
                for chunk in self.agent.run():
                    if "content" in chunk.choices[0]["delta"]:
                        content = chunk.choices[0]["delta"]["content"]
                        buffer_str += content
                        buffer.append(content)
                        buffer_show = "".join(buffer).strip()
                        if "\n" in content:
                            buffer = []
                            result += buffer_str
                            buffer_str = ""
                            buffer_show = ""

                        live.update(Markdown(result + f'*{buffer_show}*'))
                result += buffer_str
                live.update(Markdown(result))
        except Exception as exc:
            print(exc)
            exit(1)
