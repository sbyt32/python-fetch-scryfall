from fastapi import APIRouter
from typing import Union
from api_files.response_class.pretty import PrettyJSONResp
import scripts.connect.to_database as to_db
from psycopg.rows import dict_row

router = APIRouter()

# Return all group names in current use
@router.get("/", status_code=200, response_class=PrettyJSONResp)
async def get_group_names(use: Union[bool, None] = None):
    if use:
        query = """

        SELECT 
            DISTINCT(group_naming), 
            groupings.description 
        FROM 
            (
                SELECT 
                    UNNEST(groups) 
                FROM card_info.info
            )   AS a(group_naming)
        JOIN card_info.groups AS groupings
            ON groupings.group_name = group_naming
    """
    else:
        query = """
        
        SELECT 
            groups.group_name,
            groups.description
        FROM card_info.groups AS groups
        
    """
    conn, cur = to_db.connect_db(row_factory = dict_row)

    cur.execute(query)

    return cur.fetchall()