import configparser
import time
import hashlib
import json
import logging
import psycopg
import datetime
import scripts.connect.to_requests_wrapper as to_requests_wrapper
import scripts.config_reader as cfg_reader
import scripts.connect.to_database as to_db
from dateutil.parser import isoparse
log = logging.getLogger()


def fetch_tcg_prices():
    start = time.perf_counter() # ? Used for timing the length to parse everything
    cfg = cfg_reader.config_reader('UPDATES', 'database')

    conn, cur = to_db.connect_db()
    cur.execute("SELECT tcg_id, name, new_search FROM card_info.info")
    res = cur.fetchall()

    for card_data in res:
        card_id:str = card_data[0]
        card_name:str = card_data[1]
        duplicate_merge:bool = card_data[2]
        offset_value = 0
        increment = 0

        url = f"https://mpapi.tcgplayer.com/v2/product/{card_id}/latestsales"
        # ? Is there a much easier way to do more than 25? Yes, but it's a bit tougher.
        payload = {
            "listingType":"All",
            "languages": [1], # We really only support about English at the moment, opt-in language support maybe later?
            "offset":0,
            "limit":25
            }
        headers = {
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
            }

        resp = to_requests_wrapper.send_response("POST", url, json=payload, headers=headers)

        try:
            if resp['resultCount'] > 0:
                keep_adding_cards = True
        except TypeError:
            keep_adding_cards = False

        while keep_adding_cards:
            log.debug(f"Getting {card_name} data with offset of {offset_value}, recieved {resp['resultCount']} results.")
            for sale_data in resp['data']:

                order_id        = hashlib.sha256(card_id.encode('utf-8') + json.dumps(sale_data, sort_keys=True).encode('utf-8')).hexdigest()
                order_date      = sale_data['orderDate']
                condition:str       = sale_data['condition']
                variant:str         = sale_data['variant']
                qty:int             = sale_data['quantity']
                buy_price       = sale_data['purchasePrice']
                ship_price      = sale_data['shippingPrice']
                try:
                    cur.execute("""

                        INSERT INTO card_data_tcg (
                            order_id,
                            tcg_id,
                            order_date,
                            condition,
                            variant,
                            qty,
                            buy_price,
                            ship_price
                            )
                        VALUES (
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                            )

                        """, (
                            order_id,
                            card_id,
                            order_date,
                            condition,
                            variant,
                            qty,
                            buy_price,
                            ship_price
                        )
                    )

                        # TODO: Resolve this?
                        # * Ash     :  With fetch_tcg_prices(), stop committing everywhere. You should just commit changes at the end of the function
                        # * Frank   :  I think part of it was seeing that psycopg2.connection.rollback() undoes back all of the data 
                        # *            https://www.psycopg.org/docs/connection.html#connection.rollback

                        # ? Maybe this could be the answer?
                        # * https://www.psycopg.org/psycopg3/docs/basic/transactions.html#nested-transactions
                        
                except psycopg.errors.UniqueViolation:
                    # * Three checks: 
                        # We should merge because of an override like adding a new card after initial fetch (new_search under card_info.info), 
                        # If there was no previous checks performed (cfg file check), 
                        # If the data point was added after the initial fetch (cfg file check against order date).
                    if duplicate_merge == True or cfg["tcg_sales"] == 'None' or isoparse(order_date) > isoparse(cfg["tcg_sales"]):
                        conn.rollback()
                        log.warning(f"Duplicate data for card {card_name}, approx. # {offset_value} - {offset_value + 25}, merging ID {order_id}")
                        cur.execute("""

                            UPDATE card_data_tcg
                            SET qty = card_data_tcg.qty + %s
                            WHERE order_id = %s

                            """, (
                            qty,
                            order_id
                            )
                        )
                        conn.commit()
                    else:
                        log.info(f"Grabbed {increment} new data points from {card_name}.")
                        conn.rollback()
                        keep_adding_cards = False
                        stop_future_looping = """
                
                        UPDATE card_info.info SET new_search = false WHERE tcg_id = %s;

                        """
                        cur.execute(stop_future_looping, (card_id,))
                        conn.commit()
                        break
                else:
                    increment += 1
                    conn.commit()

            # * Check if we need to run it again. If the results count is less than 25, don't run. If it does not say "nextPage", don't run.
            if resp['nextPage'] == "Yes" or keep_adding_cards == False:

                offset_value += 25
                payload = {
                    "listingType":'All',
                    "languages": [1],
                    "offset":offset_value,
                    "limit":25,
                    "time":1668972898655
                    }

                resp = to_requests_wrapper.send_response("POST", url, json=payload, headers=headers)
                time.sleep(.5)
            else:
                stop_future_looping = """
                
                UPDATE card_info.info SET new_search = false WHERE tcg_id = %s;

                """
                cur.execute(stop_future_looping, (card_id,))
                conn.commit()
                keep_adding_cards = False

    # * After parsing, update the records to show the data.
    config = configparser.ConfigParser()
    config.read('config_files/database.ini')
    config['UPDATES']['tcg_sales'] = str(datetime.datetime.now(datetime.timezone.utc))
    with open('config_files/database.ini', 'w') as config_update:
        config.write(config_update)

    log.debug(f"Elapsed time: {time.perf_counter() - start}") # ? Sends length to parse to debug