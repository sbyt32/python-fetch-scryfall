import psycopg2
import psycopg2.errors
import scripts.connect.to_requests_wrapper
import scripts.connect.to_database
import logging
log = logging.getLogger()
from psycopg2 import sql
from scripts import config_reader

def check_set_exists(sets:object,cur):
    return bool(cur.execute("SELECT * from card_info.sets WHERE set = %s AND set_full = %s", (sets['code'],sets['name'])))

def _set_up():
    config = config_reader.config_reader()
    conn, cur = scripts.connect.to_database.connect()

    # Create database, if not existing.
    conn.autocommit = True

    try:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(config['CONNECT']['dbname'])))
        db_create = f"Creating database: {config['CONNECT']['dbname']}"
    except psycopg2.errors.DuplicateDatabase:
        db_create = 'Database "{config["CONNECT"]["dbname"]}" already exists.'
    finally:
        log.debug(db_create)
    conn.close()


    conn, cur = scripts.connect.to_database.connect()

    # * Schema to organize information easier
    cur.execute("CREATE SCHEMA IF NOT EXISTS card_info")
    log.debug('Creating schema "card_info" if it does not exist')

    # * Store the cards you like to track card_info.info
    cur.execute(
    """
        CREATE TABLE IF NOT EXISTS card_info.info(
            name    varchar(255),
            set     varchar(12),
            id      text
        )
    """)
    log.debug('Creating table "card_info.info" if it does not exist')

    # * Card data
    cur.execute(
    """CREATE TABLE IF NOT EXISTS card_data 
    (
        set         varchar(12) NOT NULL,
        id          text        NOT NULL,
        date        date        NOT NULL,
        usd         float(2),
        usd_foil    float(2),
        usd_etched  float(2),
        euro        float(2),
        euro_foil   float(2),
        tix         float(2)
    )""")
    log.debug('Creating table "card_data" if it does not exist')

    # * Set names, etc
    cur.execute(
    """CREATE TABLE IF NOT EXISTS card_info.sets
    (
        set             varchar(12) NOT NULL PRIMARY KEY,
        set_full        text        NOT NULL,
        release_date    date
    )""")

    log.debug('Creating table "card_info.sets" if it does not exist')


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
    log.debug('Creating table "card_info.groups" if it does not exist')

    conn.commit()
    conn.close()

    return True