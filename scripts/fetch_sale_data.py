import arrow
import uuid
import time
import hashlib
import json
import logging
import psycopg2.errors
import scripts.connect.to_requests_wrapper as to_requests_wrapper
import scripts.config_reader as cfg_reader
import scripts.connect.to_database as to_db

log = logging.getLogger()


repeat_checker = f"{arrow.utcnow().format('MM_DD_YY')}_{str(uuid.uuid4())[:8]}"
cfg = cfg_reader.config_reader()

def update_date():
    cfg['UPDATES']['TCG_SALES'] = repeat_checker
    log.info(f"Config: {'TCG_SALES'} | cfg['UPDATES']['TCG_SALES'] -> {repeat_checker}")

    with open('config.ini', 'w') as config_update:
        cfg.write(config_update)



def fetch_tcg_prices():
    # 
    try:
        # Just checking if this exists
        cfg['UPDATES']['TCG_SALES']
    except KeyError:
        log.info("Will attempt to parse all data as I assume you never fetched these cards before.")
        update_date()
    
    start = time.perf_counter()

    conn, cur = to_db.connect()
    cur.execute("SELECT tcg_id, name FROM card_info.info")
    res = cur.fetchall()

    for card_data in res:
        # * I just want the first (and really only part of this tuple)
        card_id:str = card_data[0]
        card_name:str = card_data[1]
        offset_value = 0
        increment = 0

        url = f"https://mpapi.tcgplayer.com/v2/product/{card_id}/latestsales"

        # ? Is there a much easier way to do more than 25? Yes, but it's a bit tougher.
        payload = {
            "listingType":'All',
            "offset":0,
            "limit":25,
            "time":1668972898655
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
                condition       = sale_data['condition']
                variant         = sale_data['variant']
                qty             = sale_data['quantity']
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
                        # ON CONFLICT ON CONSTRAINT card_data_tcg_order_id_key
                        # DO NOTHING
                except psycopg2.errors.UniqueViolation:
                    if cfg['UPDATES']['TCG_SALES'] == repeat_checker:
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
                        break
                else:
                    increment += 1
                    conn.commit()

            # Check if we need to run it again. If the results count is less than 25, don't run. If it does not say "nextPage", don't run.
            if resp['nextPage'] == "Yes" or keep_adding_cards == False:

                offset_value += 25
                payload = {
                    "listingType":'All',
                    "offset":offset_value,
                    "limit":25,
                    "time":1668972898655
                    }

                resp = to_requests_wrapper.send_response("POST", url, json=payload, headers=headers)
                time.sleep(.5)
            else:
                keep_adding_cards = False

    update_date()

    log.debug(f"Elapsed time: {time.perf_counter() - start}")