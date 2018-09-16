import os
import sqlite3
import re

from json import loads
from discord import utils as discord_utils, Embed
from utilities import get_file
from db_utilities import build_db, connect as db_connect

from csbot import Bot

CONFIG_FILE = 'config.json'

if not os.path.exists(CONFIG_FILE):
    print('ERROR: config.json does not exist!')
    exit(1)

config = loads(get_file(CONFIG_FILE))
announce_message_format = get_file(config['announce_message_format_file'])
mention_regex_pattern = re.compile('@(\w+)#(\d+)')

bot = Bot(config['token'])

def parse_mentions(message):
    matches = mention_regex_pattern.finditer(message.content)
    result = message.content

    channel = discord_utils.get(bot.client.get_all_channels(), id=config['general_channel_id'])
    for match in matches:
        user = discord_utils.get(channel.server.members, name=match[1], discriminator=match[2])
        span = match.span()

        result = result[:span[0]] + user.mention + result[span[1]:]

    message.content = result
    return message

def has_opted_out_announcement(user):
    conn, cursor = db_connect()

    cursor.execute("SELECT * FROM announcement_blacklist WHERE id=?", (user.id,))
    query = cursor.fetchone()
    return query != None

    conn.commit()
    conn.close()

@bot.command('announce')
async def announce_command(message, args):
    if message.author.server_permissions.administrator:
        command_less = message.content.replace('!announce',  '')
        if len(command_less) == 0: return

        announce_message = announce_message_format.format(message.author.name, command_less)

        for member in bot.client.get_all_members():
            if has_opted_out_announcement(member): continue
            
            try:
                embed = Embed(title='Computer Science Club', description='This an automated message. To opt-out, type "!optout"', color=0x0080ff)
                embed.set_thumbnail(url='https://i.imgur.com/tEZPnyZ.png')
                embed.add_field(name='Announcement', value=command_less, inline=False)
                await bot.client.send_message(member, embed=embed)
            except:
                print('Couldn\'t send message to {0}'.format(member.name))

@bot.command('optin')
async def optin_command(message, args):
    if has_opted_out_announcement(message.author):
        conn, cursor = db_connect()

        cursor.execute("DELETE FROM announcement_blacklist WHERE id=?", (message.author.id,))
            
        conn.commit()
        conn.close()

        await bot.client.send_message(message.channel, 'Successfully opted into automated notifications!')

@bot.command('optout')
async def optout_command(message, args):
    if not has_opted_out_announcement(message.author):
        conn, cursor = db_connect()

        cursor.execute("INSERT INTO announcement_blacklist (id) VALUES (?)", (message.author.id,))

        conn.commit()
        conn.close()

        await bot.client.send_message(message.channel, 'Successfully opted-out from automated notifications!')

@bot.command('show_blacklist')
async def show_blacklist_command(mesage, args):
    if message.author.server_permissions.administrator:
        conn, cursor = db_connect()

        cursor.execute("SELECT * FROM announcement_blacklist")
        query = cursor.fetchall()

        final_message = '#################\n'

        if query:
            for query_elem in query:
                user_id = query_elem[0]
                final_message += discord_utils.get(bot.client.get_all_members(), id=user_id).name  + '\n' 

        final_message += '#################'

        conn.commit()
        conn.close()

        await bot.client.send_message(message.channel, final_message)

@bot.command('ping')
async def ping_command(message, args):
    await bot.client.send_message(message.channel, 'pong')

@bot.command('send_as_lane')
async def send_as_lane(message, args):
    if message.author.id in config['authorized_users']:
        message_to_send = parse_mentions(message).content.replace('!send_as_lane',  '').strip()
        channel = discord_utils.get(bot.client.get_all_channels(), id=config['general_channel_id'])
        
        await bot.client.send_message(channel, message_to_send)

bot.run()

