
class CommandManager:
    def __init__(self):
        self.commands = {}

    def register_command(self, command: int, callback: callable):
        self.commands[command] = callback

    def execute(self, command: int, payload_type: int, payload: bytes):
        if command in self.commands:
            self.commands[command](payload_type, payload)
        else:
            raise ValueError(f"Command {command} not registered")
