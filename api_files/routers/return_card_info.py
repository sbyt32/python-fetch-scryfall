from pydantic import BaseModel
from typing import Union
from fastapi import APIRouter, Depends, HTTPException, Response, status
from api_files.dependencies import select_access
from api_files.response_models.card_info import CardInfo
import scripts.connect.to_database as to_db
import json


class PrettyJSONResp(Response):
    media_type = "application/json"

    def render(self, content) -> bytes:
        return json.dumps(content,ensure_ascii=False, allow_nan=False,indent=3,separators=(", ", ": ")).encode('utf-8')


router = APIRouter(
    prefix="/card",
    tags=["Get some card info"],
    dependencies=[Depends(select_access)],
    responses={404: {"description": "Not found"}},
)

@router.get("/", status_code=200, response_class=PrettyJSONResp, response_model=CardInfo)
async def read_items(response: Response):
    conn, cur = to_db.connect_db()
    cur.execute(""" 
        
        SELECT   
            card_info.info.name,
            card_info.sets.set_full,
            card_info.info.set,
            card_info.info.id,
            card_info.info.uri
        FROM card_info.info
        JOIN card_info.sets
            ON card_info.info.set = card_info.sets.set
        """,

        # (set, id)
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
                    'uri': cards[4]
                }
            )

        return {
            "resp"      : "card_data",
            "status"    : response.status_code,
            "data"      : card_data
        }


@router.get("/{set}/{id}")
async def read_item(set: str, id: str, response: Response):
    conn, cur = to_db.connect_db()
    cur.execute(""" 
        
        SELECT  * 
        FROM    card_info.info
        WHERE   set = %s AND id = %s

        """,

        (set, id)
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
