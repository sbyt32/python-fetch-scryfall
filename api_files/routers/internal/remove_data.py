from fastapi import APIRouter, Depends
from api_files.dependencies import write_access
from psycopg.rows import dict_row
import scripts.connect.to_database as to_db
import logging
from pydantic import BaseModel
log = logging.getLogger()
text_resp = ''


router = APIRouter(
    tags=["Remove card data."],
    dependencies=[Depends(write_access)],
    )

@router.delete("/remove/{set}/{id}")
async def remove_card_from_database(set:str, id:str):

    conn, cur = to_db.connect_db(row_factory = dict_row)

    cur.execute("SELECT name, id, set from card_info.info where id = %s AND set = %s", (id, set))

    fetched_card = cur.fetchone()
    if fetched_card:
        text_resp = f"Deleting: {fetched_card['name']} (Set: {fetched_card['set']}, Collector Num: {fetched_card['id']})"
        log.info(text_resp)
        cur.execute("DELETE FROM card_info.info WHERE id = %s AND set = %s", (id,set))
        # ? Uncomment below in production.
        conn.commit()

    else:
        text_resp = f"Failed to delete, does not exist on DB (Set: {set}, Collector Num: {id})"
        log.error(text_resp)

    return text_resp

# TODO: Move the request body to another location
class Card_Groups(BaseModel):
    set: str
    id: str
    group: str

@router.delete("/remove/groups")
async def remove_card_groups_with_set_id(card_group: Card_Groups):
    
    conn, cur = to_db.connect_db(row_factory = dict_row)

    cur.execute("SELECT name, set, id, groups from card_info.info where id = %s AND set= %s", (card_group.id, card_group.set))

    fetched_card = cur.fetchone()

    # * If the card exists and the group is associated with the card. 
    if fetched_card and card_group.group in fetched_card['group']:
        cur.execute("UPDATE card_info.info SET groups = array_remove(card_info.info.groups, %s) WHERE id = %s and set = %s", (card_group.group, card_group.id,card_group.set))
        pass