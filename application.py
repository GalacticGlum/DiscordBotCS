from json import loads
from discord import Client as DiscordClient
from utils import get_file

secrets = loads(get_file('secrets.json'))
client = DiscordClient()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user: return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(secrets['client-token'])