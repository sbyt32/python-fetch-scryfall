import csv
import arrow
import os
import psycopg2
import psycopg2.errors
from variables import HOST, USER, PASS, DBNAME



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
    insert_values = """
        INSERT INTO card_data (set, id, date, usd, usd_foil, euro, euro_foil, tix) 

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

        """
        
    cur.execute(insert_values, (set,id,arrow.utcnow().format('YYYY-MM-DD'), usd, usd_foil, eur, eur_foil, mtgo))
    conn.commit()