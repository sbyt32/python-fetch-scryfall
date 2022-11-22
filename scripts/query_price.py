import scripts.connect.to_database as to_database
import scripts.connect.to_requests_wrapper as to_requests
import arrow
import logging
from time import sleep
log = logging.getLogger()


def query_price():
    conn, cur = to_database.connect()

    cur.execute("SELECT uri FROM card_info.info")
    records = cur.fetchall()

    log.debug(f"Parsing {len(records)} cards.")
    for uri in records:
        r = to_requests.send_response('GET',uri[0])
        sleep(.2)
        insert_values = """
            INSERT INTO card_data (set, id, date, usd, usd_foil, euro, euro_foil, tix) 

            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

            """
        cur.execute(
        insert_values, (
            r['set'],
            r['collector_number'],
            arrow.utcnow().format('YYYY-MM-DD'),
            r['prices']['usd'],
            r['prices']['usd_foil'],
            r['prices']['eur'],
            r['prices']['eur_foil'],
            r['prices']['tix'],
        ))

    conn.commit()
    log.debug(f"Parsed all {len(records)} cards")
