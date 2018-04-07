from json import loads
from discord import Client as DiscordClient
from utils import get_file

config = loads(get_file('config.json'))
client = DiscordClient()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(367469096557871127) 
    await channel.send('Your favourite teacher—and bot—me—has arrived!')

@client.event
async def on_message(message):
    if message.author == client.user: return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

async def console_read_task():
    await client.wait_until_ready()

    channel = client.get_channel(367469096557871127)
    while not client.is_closed():
        message = input()
        await channel.send(message)

client.loop.create_task(console_read_task())
client.run(config['client-token'])