import psycopg
import scripts.connect.to_database as to_database
import scripts.connect.to_requests_wrapper as to_requests
import logging
from psycopg import sql
from scripts import config_reader

log = logging.getLogger()

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
    cfg = config_reader.config_reader("CONNECT", "database")
    
    # conn, cur = to_database.connect_db()
    conn = psycopg.connect(f"host={cfg['host']} user={cfg['user']} password={cfg['password']}")
    cur = conn.cursor()
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

    # * Store the cards you like to track card_info.info (this script).
    # * new_search is for TCG price data, true = merges matching data, false halts the script entirely.
    cur.execute(
    """
        CREATE TABLE IF NOT EXISTS card_info.info(
            name            varchar(255),
            set             varchar(12),
            id              text,
            uri             text,
            tcg_id          text,
            tcg_id_etch     text,
            new_search      boolean   
        )
    """)
    log.debug('Creating table "card_info.info" if it does not exist')

    # * Card data, where all of the current price information lives. 
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

    resp = to_requests.send_response('GET','https://api.scryfall.com/sets')['data']

    for sets in resp:
        if not sets['digital']:
            log.debug(f"Inserting {sets['name']} into card_info.sets")
            
            cur.execute(
                """
                INSERT INTO card_info.sets (set, set_full, release_date)

                VALUES (%s, %s, %s)
                
                ON CONFLICT DO NOTHING
                """, (sets['code'], sets['name'], sets['released_at'])
                )
        else:
            log.debug(f"Not inserting {sets['name']}: Set is digital-only.")

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