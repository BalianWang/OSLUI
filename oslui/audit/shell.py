from oslui.action import ShellCommand
from oslui.audit import BaseAuditor


class ShellAuditor(BaseAuditor):
    def __init__(self):
        # 初始化一些审计规则
        super().__init__()
        self.danger_keywords = ['rm', 'chmod', 'chown',
                                '|', '&', '>', '>>', '<', 'eval', '`', '$(', ';']

    def audit(self, command: ShellCommand):
        cmd_content = command.content
        for keyword in self.danger_keywords:
            if keyword in command:
                return False

        # 不允许执行外部命令或绝对路径，只允许执行系统内置的命令
        if '/' in command and not cmd_content.startswith('/bin/') and not cmd_content.startswith('/usr/bin/'):
            return False

        # 不允许包含变量或通配符
        if '$' in command or '*' in command:
            return False

        # 可以添加更多自定义的审计规则，根据您的需求和系统安全要求

        return True
