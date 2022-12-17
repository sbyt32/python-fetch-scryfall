from fastapi import APIRouter, Depends, HTTPException
from api_files.dependencies import write_access
from psycopg.rows import dict_row
import scripts.connect.to_database as to_db
import scripts.connect.to_requests_wrapper as to_requests_wrapper
from pydantic import BaseModel
import logging
log = logging.getLogger()

router = APIRouter(
    tags=["Add some cards to track"],
    )

# Add some cards with the set and ID of the card
@router.post("/add/{set}/{id}")
async def add_card_to_track_with_set_id(set: str, id:str):

    resp = to_requests_wrapper.send_response('GET',f"https://api.scryfall.com/cards/search?q=set:{set}+cn:{id}")

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
            error_msg = f"Recieved list with more than 1. Set:{set}, ID:{id}"
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


# TODO: Move the request body to another location
# * https://fastapi.tiangolo.com/tutorial/body/#__tabbed_2_1
class Card_Groups(BaseModel):
    set: str
    id: str
    group: str


@router.post("/add/groups")
async def add_card_groups_with_set_id(card_group: Card_Groups):
    text_resp = ''

    conn, cur = to_db.connect_db(row_factory = dict_row)

    cur.execute("SELECT name, set, id, groups from card_info.info where id = %s AND set= %s", (card_group.id, card_group.set))

    fetched_card = cur.fetchone()
    # * If the card doesn't already have a group, it'll return Null/None.
    if fetched_card['groups'] == None:
        fetched_card['groups'] = []

    # * If the card exists and the group is not associated with the card.
    if fetched_card and not card_group.group in fetched_card['groups']:
        cur.execute("UPDATE card_info.info SET groups = array_append(card_info.info.groups, %s) WHERE id = %s and set = %s", (card_group.group, card_group.id,card_group.set))
        conn.commit()

        text_resp = f"{fetched_card['name']} (Set: {fetched_card['set']}, Collector Num: {fetched_card['id']}) is now associated with the groups: {fetched_card['groups'] + [card_group.group]}"    
        log.info(text_resp)

    # * Warning if the group is already with the card
    elif card_group.group in fetched_card['groups']:
        text_resp = f"{fetched_card['name']} (Set: {fetched_card['set']}, Collector Num: {fetched_card['id']}) already is associated with the group: {fetched_card['groups']}"
        log.warning(text_resp)

    # * If the card doesn't exist on the database. It might exist as a card, though.
    elif fetched_card == None:
        text_resp = f"Set: {card_group.set}, Collector Num: {card_group.id} does not exist on the database!"
        log.error(text_resp)

    # * Just in case, I'm not too sure what would trigger this?
    else:
        text_resp = f"Uncertain error returned. Logging response to look over later."
        log.error(text_resp)

    return text_resp
