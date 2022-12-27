from api_files.request_models.card_groups_model import CardGroups
from fastapi import APIRouter, Depends, HTTPException
from psycopg.rows import dict_row
import scripts.connect.to_database as to_db
import scripts.connect.to_requests_wrapper as to_requests_wrapper
import logging
log = logging.getLogger()


router = APIRouter()

@router.post("/add/groups")
async def add_card_groups_with_set_id(card_group: CardGroups):
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
