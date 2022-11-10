import psycopg2
import psycopg2.errors
import scripts
import scripts.request_wrapper
from psycopg2 import sql


def check_set_exists(sets:object,cur):
    return bool(cur.execute("SELECT * from card_info.sets WHERE set = %s AND set_full = %s", (sets['code'],sets['name'])))

def _set_up():
    config = scripts.config_reader()
    HOST = config['CONNECT']['host']
    USER = config['CONNECT']['user']
    PASS = config['CONNECT']['pass']
    DBNAME = config['CONNECT']['dbname']
    # * Have to create a database first, to separate everything. 
    conn = psycopg2.connect(user=USER, password=PASS, host=HOST)
    cur = conn.cursor()
    conn.autocommit = True
    try:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DBNAME)))
    except psycopg2.errors.DuplicateDatabase:
        pass
    conn.close()

    conn = psycopg2.connect(dbname = DBNAME, user=USER, password=PASS, host=HOST)
    cur = conn.cursor()
    
    # * Schema to organize information easier
    cur.execute("CREATE SCHEMA IF NOT EXISTS card_info")
    # * Store the cards you like to track card_info.info
    cur.execute(
    """
        CREATE TABLE IF NOT EXISTS card_info.info(
            name    varchar(255),
            set     varchar(12),
            id      text,
            uri     text
        )
    """)
    # * Card data
    cur.execute(
    """CREATE TABLE IF NOT EXISTS card_data 
    (
        set         varchar(12) NOT NULL,
        id          text        NOT NULL,
        date        date        NOT NULL,
        usd         float(2),
        usd_foil    float(2),
        euro        float(2),
        euro_foil   float(2),
        tix         float(2)
    )""")

    # * Set names, etc
    cur.execute(
    """CREATE TABLE IF NOT EXISTS card_info.sets
    (
        set             varchar(12) NOT NULL PRIMARY KEY,
        set_full        text        NOT NULL,
        release_date    date
    )""")

    resp = scripts.request_wrapper.send_response('https://api.scryfall.com/sets')['data']
    for sets in resp:
        if not sets['digital']:
            
            if check_set_exists(sets, cur) == False:
                
                cur.execute(
                    """
                    INSERT INTO card_info.sets (set, set_full, release_date)

                    VALUES (%s, %s, %s)
                    
                    ON CONFLICT DO NOTHING
                    """, (sets['code'], sets['name'], sets['released_at'])
                    )

    # * This creates the card_info.groups table, which organizes popular groupings, such as "fetchland" or "shockland".
    cur.execute(
        """ CREATE TABLE IF NOT EXISTS card_info.groups
        (
            id      text        NOT NULL,
            set     varchar(12) NOT NULL,
            groups  text[]
        
        )""")

    conn.commit()