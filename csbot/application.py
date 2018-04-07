from json import loads
from discord import Client as DiscordClient
from utils import get_file

config = loads(get_file('../config.json'))
client = DiscordClient()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user: return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(config['client-token'])