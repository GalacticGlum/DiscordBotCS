from discord import Client as DiscordClient
from db_utilities import build_db

class Bot(object):
    def __init__(self, token):
        self.commands = {}
        self.token = token
        self.client = DiscordClient()
        build_db()

    def run(self):
        @self.client.event
        async def on_message(message):
            if message.author == self.client.user: return

            command, args = Bot.__extract_command(message.content)
            if command and command in self.commands:
                await self.commands[command](message, args)

        self.client.run(self.token)

    def __add_command(self, command, identifier, handler_func):
        full_command = identifier + command
        if full_command in self.commands:
            print('Command with name \'{0}\' already exists!'.format(full_command))
            return

        self.commands[full_command] = handler_func

    def command(self, name, identifier='!'):
        def wrapper(func):
            self.__add_command(name, identifier, func)
            return func

        return wrapper

    @staticmethod
    def __extract_command(message_str):
        parts = message_str.strip().split()
        return (None, None) if len(parts) == 0 else (parts[0], parts[1:])