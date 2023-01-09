from fastapi import APIRouter, HTTPException, Response, status
from api_files.response_models.card_info import CardInfo
from api_files.response_class.pretty import PrettyJSONResp
from psycopg.rows import dict_row
import scripts.connect.to_database as to_db

router = APIRouter(
    prefix="/search"
)

# Return all cards
@router.get(
    path="/", 
    status_code=200, 
    response_class=PrettyJSONResp, 
    response_model=CardInfo, 
    description="Return all cards that are being tracked.")
async def read_items(response: Response):
    conn, cur = to_db.connect_db()
    cur.execute(""" 
        
        SELECT   
            card_info.info.name,
            card_info.sets.set_full,
            card_info.info.set,
            card_info.info.id,
            card_info.info.groups
        FROM card_info.info
        JOIN card_info.sets
            ON card_info.info.set = card_info.sets.set
        """
        )
    resp = cur.fetchall()
    if resp == ():
        return {}
    else:
        response.status_code = status.HTTP_200_OK
        card_data = []
        for cards in resp:
            card_data.append(
                {
                    'name': cards[0],
                    'set_full': cards[1],
                    'set': cards[2],
                    'id': cards[3],
                    'groups': cards[4]
                }
            )

        return {
            "resp"      : "card_data",
            "status"    : response.status_code,
            "data"      : card_data
        }

# Filter for cards by their grouping.
@router.get("/{group}")
async def find_by_group(group: str):
    conn, cur = to_db.connect_db(row_factory = dict_row)
    cur.execute(""" 
        
        SELECT   
            DISTINCT ON (info.name, info.id) "name",
            sets.set_full AS "set",
            prices.date "last_updated",
            prices.usd,
            prices.usd_foil,
            prices.euro,
            prices.euro_foil,
            prices.tix
        FROM card_info.info AS "info"
        JOIN card_info.sets AS "sets"
            ON info.set = sets.set
        JOIN 
            (
                SELECT
                    prices.date,
                    prices.set,
                    prices.id,
                    prices.usd,
                    prices.usd_foil,
                    prices.euro,
                    prices.euro_foil,
                    prices.tix
                FROM 
                    card_data as "prices"
            ) AS "prices"
        ON prices.set = info.set
        AND prices.id = info.id
        WHERE %s = ANY (info.groups)
        ORDER BY 
            info.name, 
            info.id, 
            prices.date DESC

        """,
        (group,)
        )
    resp = cur.fetchall()
    if resp == []:
        return [{}]
    else:
        return resp

# Filter for cards by their set + id combo
@router.get("/{set}/{col_num}",
    description="Look for a specific card based on that cards set + collector number"
    )
async def search_by_set_collector_num(set: str, col_num: str, response: Response):
    conn, cur = to_db.connect_db()
    cur.execute(""" 
        
        SELECT  * 
        FROM    card_info.info
        WHERE   set = %s AND id = %s

        """,

        (set, col_num)
        )
    
    result = cur.fetchone()
    if result == None:
        raise HTTPException(status_code=404, detail="This card does not exist on the database!")
    else:
        response.status_code = status.HTTP_200_OK
        return {
            "resp"      : "card_data",
            "status"    : response.status_code,
            "data"      : {
                "name"      : result[0],
                "set"       : result[1],
                "id"        : result[2],
                "URL"       : result[3]
            }

        }
