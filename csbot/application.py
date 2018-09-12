import os
import sqlite3

from json import loads
from discord import Client as DiscordClient, utils as discord_utils, Embed
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

def is_command(message, command, identifier='!'):
    if not message.content.startswith(identifier): return False

    parts = message.content.split()
    if len(parts) == 0: return False
    return parts[0] == command

def has_opted_out_announcement(user):
    conn, cursor = db_connect()

    cursor.execute("SELECT * FROM announcement_blacklist WHERE id=?", (user.id,))
    query = cursor.fetchone()
    return query != None

    conn.commit()
    conn.close()

async def message_announcement(message):
    command_less = message.content.replace('!announce',  '')
    if len(command_less) == 0: return

    announce_message = announce_message_format.format(message.author.name, command_less)

    for member in client.get_all_members():
        if has_opted_out_announcement(member): continue
        
        try:
            embed = Embed(title='Computer Science Club', description='This an automated message. To opt-out, type "!optout"', color=0x0080ff)
            embed.set_thumbnail(url='https://i.imgur.com/tEZPnyZ.png')
            embed.add_field(name='Announcement', value=command_less, inline=False)
            await client.send_message(member, embed=embed)
        except:
            print('Couldn\'t send message to {0}'.format(member.name))

@client.event
async def on_message(message):
    if message.author == client.user: return
    if is_command(message, '!announce'):
        if message.author.server_permissions.administrator:
            await message_announcement(message)
    elif is_command(message, '!optout'):  
        if not has_opted_out_announcement(message.author):
            conn, cursor = db_connect()

            cursor.execute("INSERT INTO announcement_blacklist (id) VALUES (?)", (message.author.id,))

            conn.commit()
            conn.close()

            await client.send_message(message.channel, 'Successfully opted-out from automated notifications!')
    elif is_command(message, '!optin'):
        if has_opted_out_announcement(message.author):
            conn, cursor = db_connect()

            cursor.execute("DELETE FROM announcement_blacklist WHERE id=?", (message.author.id,))
                
            conn.commit()
            conn.close()

            await client.send_message(message.channel, 'Successfully opted into automated notifications!')


async def console_read_task():
    await client.wait_until_ready()

    while not client.is_closed:
        message = str()
        try:
            message = input()
        except:
            continue

        if message.strip() == 'blacklist':
            conn, cursor = db_connect()

            cursor.execute("SELECT * FROM announcement_blacklist")
            query = cursor.fetchall()
            if query:
                for query_elem in query:
                    user_id = query_elem[0]
                    print(discord_utils.get(client.get_all_members(), id=user_id).name)

            conn.commit()
            conn.close()

            print('##############\n')


client.loop.create_task(console_read_task())

client.run(config['token'])

