import csv
import arrow
import os
import psycopg2
import psycopg2.errors
from variables import HOST, USER, PASS, DBNAME


def null_check(value):

    # Scryfall can return None as an option if values don't exist. Use that.
    if value == None:
        return 'NULL'
    return f'{value}'

def append_cards(r:list):

    conn = psycopg2.connect(dbname = DBNAME, user=USER, password=PASS, host=HOST)
    cur = conn.cursor()
    set         =   r['set']
    id          =   r['collector_number']
    usd         =   r['prices']['usd']
    usd_foil    =   r['prices']['usd_foil']
    eur         =   r['prices']['eur']
    eur_foil    =   r['prices']['eur_foil']
    mtgo        =   r['prices']['tix']

        # TODO: Here should the check if it's less than 24hr
        # ? May not be nessecary, if running through crontab?
        
    # set, id, date, usd, usd_foil, eur, eur_foil, tix
    cur.execute(
    f""" 
    INSERT INTO card_data (set, id, date, usd, usd_foil, euro, euro_foil, tix) 

    VALUES (
        '{set}',
        '{id}',
        '{arrow.utcnow().format('YYYY-MM-DD')}',
        {null_check(usd)},
        {null_check(usd_foil)},
        {null_check(eur)},
        {null_check(eur_foil)},
        {null_check(mtgo)}
    )
    """
    )
    conn.commit()