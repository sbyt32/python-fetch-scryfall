from fastapi import APIRouter, HTTPException
from psycopg.rows import dict_row
import scripts.connect.to_database as to_db
import scripts.connect.to_requests_wrapper as to_requests_wrapper
import logging
log = logging.getLogger()

router = APIRouter()

# Add some cards with the set and ID of the card
@router.post("/add/{set}/{coll_num}")
async def add_card_to_track_with_set_id(set: str, coll_num:str):

    resp = to_requests_wrapper.send_response('GET',f"https://api.scryfall.com/cards/search?q=set:{set}+cn:{coll_num}")

    try:
        if resp['object'] != "list":
            log.error("Not a card!")
            raise HTTPException(
                status_code=404, detail="This is not a card!"
            )

    except KeyError as e:
        # ? What does this look like, again?
        log.error(f"KeyError:{e}")

    else:
        if not resp['total_cards'] == 1:
            error_msg = f"Recieved list with more than 1. Set:{set}, ID:{coll_num}"
            log.error(error_msg)
            return error_msg

        resp = resp['data'][0]
        conn, cur = to_db.connect_db()

        cur.execute("SELECT * from card_info.info where id = %s AND set= %s", (resp['collector_number'], resp['set']))
        if len(cur.fetchall()) == 0:
                # tcg_etched_id = ''
                try:
                    resp['tcgplayer_etched_id']
                except KeyError:
                    tcg_etched_id = None
                else:
                    tcg_etched_id = resp['tcgplayer_etched_id']
                    
                add_info_to_postgres = """
                    INSERT INTO card_info.info (name, set, id, uri, tcg_id, tcg_id_etch, new_search)

                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    """
                # ? Uncomment below in production.
                cur.execute(add_info_to_postgres, (resp['name'], resp['set'], resp['collector_number'], resp['id'], resp['tcgplayer_id'], tcg_etched_id, True))
                conn.commit()

                log.info(f'Now tracking: {resp["name"]} from {resp["set_name"]}')
                return f'Now tracking: {resp["name"]} from {resp["set_name"]}'

        else:
            log.info(f'Already tracking: {resp["name"]} from {resp["set_name"]}')
            return f'Already tracking: {resp["name"]} from {resp["set_name"]}'



@router.delete("/remove/{set}/{coll_num}")
async def remove_card_from_database(set:str, coll_num:str):

    conn, cur = to_db.connect_db(row_factory = dict_row)

    cur.execute("SELECT name, id, set from card_info.info where id = %s AND set = %s", (coll_num, set))

    fetched_card = cur.fetchone()
    if fetched_card:
        text_resp = f"Deleting: {fetched_card['name']} (Set: {fetched_card['set']}, Collector Num: {fetched_card['id']})"
        log.info(text_resp)
        cur.execute("DELETE FROM card_info.info WHERE id = %s AND set = %s", (coll_num,set))
        conn.commit()

    else:
        text_resp = f"Failed to delete, does not exist on DB (Set: {set}, Collector Num: {coll_num})"
        log.error(text_resp)

    return text_resp

