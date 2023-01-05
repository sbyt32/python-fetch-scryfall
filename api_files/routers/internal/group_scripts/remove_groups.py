from fastapi import APIRouter, Depends
from api_files.request_models.card_groups_model import CardGroups
from psycopg.rows import dict_row
import scripts.connect.to_database as to_db
import logging
log = logging.getLogger()

router = APIRouter(

)

@router.delete("/remove/groups")
async def remove_card_groups_with_set_id(card_group: CardGroups):
    
    conn, cur = to_db.connect_db(row_factory = dict_row)

    cur.execute("SELECT name, set, id, groups from card_info.info where id = %s AND set= %s", (card_group.id, card_group.set))

    fetched_card = cur.fetchone()

    # * If the card exists and the group is associated with the card. 
    if fetched_card and card_group.group in fetched_card['group']:
        cur.execute("UPDATE card_info.info SET groups = array_remove(card_info.info.groups, %s) WHERE id = %s and set = %s", (card_group.group, card_group.id,card_group.set))
        pass