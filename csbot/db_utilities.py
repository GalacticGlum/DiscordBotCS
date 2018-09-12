import sqlite3

def connect():
    conn = sqlite3.connect('cs_bot.db')
    cursor = conn.cursor()

    return conn, cursor

def build_db():
    conn, cursor = connect()

    cursor.execute('CREATE TABLE IF NOT EXISTS announcement_blacklist (id VARCHAR(512) NOT NULL, PRIMARY KEY (id))')
    
    conn.commit()
    conn.close()