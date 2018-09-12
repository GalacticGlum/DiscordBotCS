import os
import sqlite3

from json import loads
from discord import Client as DiscordClient, utils as discord_utils
from utilities import get_file
from db_utilities import build_db, connect as db_connect

CONFIG_FILE = 'config.json'

if not os.path.exists(CONFIG_FILE):
    print('ERROR: config.json does not exist!')
    exit(1)

config = loads(get_file(CONFIG_FILE))
announce_message_format = get_file(config['announce_message_format_file'])

client = DiscordClient()
build_db()

# @client.event
# async def on_ready():
#     pass


def has_opted_out_announcement(user):
    conn, cursor = db_connect()

    cursor.execute("SELECT * FROM announcement_blacklist WHERE id=?", (user.id,))
    query = cursor.fetchone()
    return query != None

    conn.commit()
    conn.close()

async def message_announcement(message):
    announce_message = announce_message_format.format(message.author.name, message.content.replace('!announce',  ''))
    
    # for member in client.get_all_members():
    #     client.send_message(member, announce_message)

    if has_opted_out_announcement(discord_utils.get(client.get_all_members(), id='131869972740833280')): return
    await client.send_message(discord_utils.get(client.get_all_members(), id='131869972740833280'), announce_message)

@client.event
async def on_message(message):
    if message.author == client.user: return
    if message.content.split()[0] == '!announce':
        await message_announcement(message)
    elif message.content.split()[0] == '!optout':
        conn, cursor = db_connect()
        
        cursor.execute("INSERT INTO announcement_blacklist (id) VALUES (?)", (message.author.id))

        conn.commit()
        conn.close()

# async def console_read_task():
#     await client.wait_until_ready()

#     channel = client.get_channel(367469096557871127)
#     while not client.is_closed():
#         message = input()
#         await channel.send(message)

# client.loop.create_task(console_read_task())

client.run(config['token'])