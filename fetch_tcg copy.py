import requests
from time import sleep
import scripts.connect.to_database as to_db


conn, cur = to_db.connect()
cur.execute(
    """
    SELECT tcg_id
    FROM card_info.info
    """
    )
res = cur.fetchall()

for card in res:
    # * I just want the first (and really only part of this tuple)
    card = card[0]

    url = f"https://mpapi.tcgplayer.com/v2/product/{card}/latestsales"

    # ? So, this is an issue because it won't return a certain value.
    payload = "{listingType:'All',offset:0,limit:-101,time:1668972898655}"
    headers = {
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    resp = response.json()

    # TODO: Check the amount of cards that exist, then work backwards
    total_cards:int = resp['totalResults']
    if total_cards <= 101:
        pass
    else:
        search_offset = total_cards + 101
        # This will get incorrect once we reach the end.

        while not search_offset == total_cards:
            # TODO: when this hits below 100, this will fetch the first 100 results, leading to duplicate
            payload = {"listingType":"All","offset":search_offset,"limit":-101,"time":1668972898655}
            headers = {
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
            }

            response = requests.request("POST", url, json=payload, headers=headers)
            # if not response.ok:
            #     print(response.text)
            #     break
            resp = response.json()
            # print(resp)
            # break
            search_offset -= 100
            if search_offset <= 0:
                search_offset = 0
            print(f'hello offset is {search_offset}')
            for sold_card in resp['data']:
                order_date = sold_card['orderDate']
                condition = sold_card['condition']
                variant = sold_card['variant']
                qty = sold_card['quantity']
                buy_price = sold_card['purchasePrice']
                ship_price = sold_card['shippingPrice']
                
                cur.execute("""

                    INSERT INTO card_data_tcg (tcg_id, order_date, condition, variant, qty, buy_price, ship_price)
                    VALUES (%s, %s, %s, %s, %s,%s,%s)

                """, (card, order_date, condition,variant,qty,buy_price,ship_price))
                conn.commit()
            sleep(1)
        pass
    # offset = 0
 
    # for sold_card in resp['data']:
    #     order_date = sold_card['orderDate']
    #     condition = sold_card['condition']
    #     variant = sold_card['variant']
    #     qty = sold_card['quantity']
    #     buy_price = sold_card['purchasePrice']
    #     ship_price = sold_card['shippingPrice']
    #     cur.execute("""

    #         INSERT INTO card_data_tcg (tcg_id, order_date, condition, variant, qty, buy_price, ship_price)
    #         VALUES (%s, %s, %s, %s, %s,%s,%s)

    #     """, (card, order_date, condition,variant,qty,buy_price,ship_price))
    #     conn.commit()
    #     break
    break
