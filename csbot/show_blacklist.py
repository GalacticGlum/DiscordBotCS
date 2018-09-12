from db_utilities import connect as db_connect
from discord import utils as discord_utils

import application

conn, cursor = db_connect()

cursor.execute("SELECT * FROM announcement_blacklist")
query = cursor.fetchall()
members = application.client.get_all_members()

if query:
    for query_elem in query:
        user_id = query_elem[0]
        print(discord_utils.get(members, id=user_id).name)

conn.commit()
conn.close()
exit(1)