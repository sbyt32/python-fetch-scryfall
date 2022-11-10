import arrow
import psycopg2
import psycopg2.errors
from scripts.config_reader import config_reader

def append_cards(r:list):
    config = config_reader()

    conn = psycopg2.connect(
        host    =   config['CONNECT']['host'],
        user    =   config['CONNECT']['user'],
        password=   config['CONNECT']['pass'],
        dbname  =   config['CONNECT']['dbname']
        )
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
        

    insert_values = """
        INSERT INTO card_data (set, id, date, usd, usd_foil, euro, euro_foil, tix) 

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

        """
        
    cur.execute(insert_values, (set,id,arrow.utcnow().format('YYYY-MM-DD'), usd, usd_foil, eur, eur_foil, mtgo))
    conn.commit()