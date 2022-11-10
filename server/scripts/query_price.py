import scripts
import psycopg2
import scripts.config_reader
from time import sleep


def query_price():
    config = scripts.config_reader.config_reader()

    conn = psycopg2.connect(host        =   config['CONNECT']['host'],
                            user        =   config['CONNECT']['user'],
                            password    =   config['CONNECT']['pass'],
                            dbname      =   config['CONNECT']['dbname']
                            )
    cur = conn.cursor()

    cur.execute("SELECT uri FROM card_info.info")
    records = cur.fetchall()

    for uri in records:
        r = scripts.send_response(uri[0])
        sleep(.2)
        scripts.append_cards(r)