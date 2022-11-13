from fastapi import APIRouter, Depends, HTTPException, Response
from dependencies import select_access
import scripts.connect.to_database as to_database
import json

class PrettyJSONResp(Response):
    media_type = "application/json"

    def render(self, content) -> bytes:
        return json.dumps(content,ensure_ascii=False, allow_nan=False,indent=3,separators=(", ", ": ")).encode('utf-8')


router = APIRouter(
    prefix="/card",
    dependencies=[Depends(select_access)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=200, response_class=PrettyJSONResp)
async def read_items():
    raise HTTPException(status_code=400, detail="Buddy this ain't the right way to get the cards.")


@router.get("/{set}/{id}")
async def read_item(set: str, id: str):
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
        return {
            "name"  : result[0],
            "set"   : result[1],
            "id"    : result[2],
            "URL"   : result[3]
        }

