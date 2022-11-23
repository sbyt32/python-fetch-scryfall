import psycopg
import scripts.connect.to_database as to_database
import scripts.connect.to_requests_wrapper as to_requests
import logging
log = logging.getLogger()
from psycopg2 import sql
from scripts import config_reader

def check_set_exists(sets:object,cur):
    return bool(cur.execute("SELECT * from card_info.sets WHERE set = %s AND set_full = %s", (sets['code'],sets['name'])))

def _set_up_db():
    """
    Creates the database, etc. Info below.
    

    | Name             | Type     | Desc                                                                     |
    |------------------|----------|--------------------------------------------------------------------------|
    | {database name}  | Database | The name of your database                                                |
    | card_data        | Table    | public schema, holds card price data. Fetched daily via Scryfall         |
    | card_data_tcg    | Table    | public schema, grabs recent sales from TCGPlayer. Fetched weekly         |
    | card_info        | Schema   | A schema to separate the price data and the information that supports it |
    | card_info.info   | Table    | card_info schema, holds identifiying information formation for cards     |
    | card_info.sets   | Table    | card_info schema, holds the names of sets and information about them     |
    | card_info.groups | Table    | card_info schema, does nothing at the moment                             |

    """
    # config = config_reader.config_reader()
    cfg = config_reader.config_reader("CONNECT", "database")
    # conn, cur = scripts.connect.to_database.connect()
    conn, cur = to_database.connect_db()

    # Create database, if not existing.
    conn.autocommit = True

    try:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(cfg['dbname'])))
        db_create = f"Creating database: {cfg['dbname']}"
    except psycopg.errors.DuplicateDatabase:
        db_create = f'Database "{cfg["dbname"]}" already exists.'
    finally:
        log.debug(db_create)
    conn.close()

    conn, cur = to_database.connect_db()

    # * Schema to organize information easier
    cur.execute("CREATE SCHEMA IF NOT EXISTS card_info")
    log.debug('Creating schema "card_info" if it does not exist')

    # * Store the cards you like to track card_info.info
    cur.execute(
    """
        CREATE TABLE IF NOT EXISTS card_info.info(
            name            varchar(255),
            set             varchar(12),
            id              text,
            tcg_id          text,
            tcg_id_etch     text
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
        usd_etch    float(2),
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

    # resp = scripts.request_wrapper.send_response('https://api.scryfall.com/sets')['data']
    # resp = scripts.connect.to_requests_wrapper.send_response('GET','https://api.scryfall.com/sets')['data']
    resp = to_requests.send_response('GET','https://api.scryfall.com/sets')['data']

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
    log.debug('Creating table "card_info.groups" if it does not exist')
    cur.execute(
        """ CREATE TABLE IF NOT EXISTS card_info.groups
        (
            id      text        NOT NULL,
            set     varchar(12) NOT NULL,
            groups  text[]
        )
        """
    )

    # * This will create the card_data_tcg table, which will pull recent sales from TCGplayer.
    log.debug('Creating table "card_data_tcg" if it does not exist')
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS card_data_tcg
        (
            order_id    varchar     NOT NULL,
            tcg_id      text        NOT NULL,
            order_date  timestamptz NOT NULL,
            condition   text        NOT NULL,
            variant     text        NOT NULL,
            qty         smallint    NOT NULL,
            buy_price   float(2)    NOT NULL,
            ship_price  float(2)    NOT NULL,
        
            UNIQUE(order_id)
        )
        """
    )
    conn.commit()
    conn.close()

    return True