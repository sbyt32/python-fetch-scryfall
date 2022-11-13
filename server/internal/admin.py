from fastapi import APIRouter, Depends, HTTPException
import scripts.connect.to_database as to_database
import scripts.connect.to_requests_wrapper as to_requests_wrapper
import logging
log = logging.getLogger()
router = APIRouter()

# ? Should internal files 

# Add a card
@router.post(
    "/add/{url}"
    )
async def add_card_to_track(url: str):

    resp = to_requests_wrapper.send_response(f"https://api.scryfall.com/cards/{url}")

    try:

        if resp['object'] != "card":
            log.error("Not a card!")
            raise HTTPException(
                status_code=404, detail="This is not a card!", status=404
            )

    except KeyError as e:
        # ? What does this look like, again?
        log.error(f"KeyError:{e}")

    else:
        conn, cur = to_database.connect()

        cur.execute("SELECT * from card_info.info where id = %s AND set= %s", (resp['id'], resp['set']))
        if len(cur.fetchall()) == 0:
        
            add_info_to_postgres = """
                INSERT INTO card_info.info (name, set, id, uri)

                VALUES (%s,%s,%s,%s)
                """
            # ? Uncomment below in production.
            # cur.execute(add_info_to_postgres, (resp['name'], resp['set'], resp['id'], resp['uri']))
            # conn.commit()

            log.info(f'Now tracking: {resp["name"]} from {resp["set_name"]}')
            return f'Now tracking: {resp["name"]} from {resp["set_name"]}'

        else:
            log.info(f'Already tracking: {resp["name"]} from {resp["set_name"]}')
            return f'Already tracking: {resp["name"]} from {resp["set_name"]}'

@router.delete("/remove/{set}/{id}")
async def remove_card(set:str, id:str):
    conn, cur = to_database.connect()

    cur.execute("SELECT * from card_info.info where id = %s AND set = %s", (id, set))
    card = cur.fetchone()
    if not card:
        log.warning(f"Failed to delete card with id: {id} and set: {set}")
    else:
        log.info(f"Deleting: {card[0]} from set: {str(card[1]).upper()}")
        cur.execute("DELETE FROM card_info.info WHERE id = %s AND set = %s", (id,set))
        # ? Uncomment below in production.
        # conn.commit()
