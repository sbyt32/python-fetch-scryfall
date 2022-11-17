from fastapi import APIRouter, Depends, HTTPException, Response, status
from dependencies import select_access
from exceptions import RootException
import scripts.connect.to_database as to_database
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

@router.get("/", status_code=200, response_class=PrettyJSONResp)
async def read_items():
    raise RootException


@router.get("/{set}/{id}")
async def read_item(set: str, id: str, response: Response):
    conn, cur = to_database.connect()
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
            "name"      : result[0],
            "set"       : result[1],
            "id"        : result[2],
            "URL"       : result[3]
        }

