import psycopg2
import scripts
import re
from operator import itemgetter
from variables import HOST, USER, PASS, DBNAME

def apost_fix(set:str):
    set = re.sub(r"'", "''", set)
    return set

def _set_up():
    conn = psycopg2.connect(dbname = DBNAME, user=USER, password=PASS, host=HOST)
    cur = conn.cursor()
    
    # Schema to organize information easier
    cur.execute("CREATE SCHEMA IF NOT EXISTS card_info")
    # Store the cards you like to track
    cur.execute(
    """
        CREATE TABLE IF NOT EXISTS card_info.info(
            name varchar(255),
            set varchar(12),
            id text,
            uri text
        )
    """)
    # Card data
    cur.execute(
    """CREATE TABLE IF NOT EXISTS card_data 
    (
        set varchar(12) NOT NULL,
        id text NOT NULL,
        date date NOT NULL,
        usd float(2),
        usd_foil float(2),
        euro float(2),
        euro_foil float(2),
        tix float(2)
    )""")

    # Set names, etc
    cur.execute(
    """CREATE TABLE IF NOT EXISTS card_info.sets
    (
        set varchar(12) NOT NULL,
        set_full text NOT NULL,
        release_date date
    )""")

    resp = scripts.util_send_response('https://api.scryfall.com/sets')['data']
    for sets in resp:
        if not sets['digital']:
            if bool(cur.execute(f"SELECT * from card_info.sets WHERE set='{sets['code']}' AND set_full='{apost_fix(sets['name'])}' ")) == False:
                cur.execute(
                    f"""
                    INSERT INTO card_info.sets (set, set_full, release_date)

                    VALUES (
                        '{sets['code']}',
                        '{apost_fix(sets['name'])}',
                        '{sets['released_at']}'
                    )
                    """)
    conn.commit()