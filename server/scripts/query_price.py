from time import sleep
import scripts
import psycopg2
from variables import HOST, USER, PASS, DBNAME

def query_price():
    conn = psycopg2.connect(dbname = DBNAME, user=USER, password=PASS, host=HOST)
    cur = conn.cursor()

    cur.execute("SELECT uri FROM card_info.info")
    records = cur.fetchall()

    for uri in records:
        r = scripts.send_response(uri[0])
        sleep(.2)
        scripts.append_cards(r)