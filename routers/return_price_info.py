from fastapi import APIRouter, Depends, HTTPException, Response
from psycopg2.errors import DatetimeFieldOverflow
from dependencies import price_access
from typing import Union
import scripts.connect.to_database as to_database
from routers.pretty import PrettyJSONResp
import logging
import re
log = logging.getLogger()

router = APIRouter(
    prefix="/price",
    dependencies=[Depends(price_access)],
    tags=["Fetch card prices"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", status_code=200, response_class=PrettyJSONResp)
async def read_items():
    raise HTTPException(status_code=400, detail="Buddy this ain't the right way to get the price data.")

@router.get("/by/{date}",  description="Get the price data for the a certain day. YYYY-MM-DD format.")
async def get_single_day_data(date:str):
    if not re.match(r'^\d\d\d\d-(0?[1-9]|[1][0-2])-(0?[1-9]|[12][0-9]|3[01])', date):
        raise HTTPException(status_code=400, detail="Incorrect format.")
    else:
        conn, cur = to_database.connect()
        try:
            cur.execute("""

                SELECT 
                    card_info.info.name,
                    card_info.sets.set_full,
                    card_info.info.id,
                    usd,
                    usd_foil,
                    euro,
                    euro_foil,
                    tix 
                FROM card_data
                JOIN card_info.info
                    ON card_data.set = card_info.info.set
                    AND card_data.id = card_info.info.id
                JOIN card_info.sets
                    ON card_data.set = card_info.sets.set
                WHERE
                    date = %s

            """, (date,))
        except DatetimeFieldOverflow as e:
            pass 

        resp = cur.fetchall()
        if resp == ():
            raise HTTPException(status_code=404, detail=f"There is no price data for {date}")
        else:
            price_data_single_day = []
            for cards in resp:
                price_data_single_day.append(
                    {
                    'name' : cards[0],
                    'set' : cards[1],
                    'collector_id': cards[2],
                    'price': {
                        'usd' : cards[3],
                        'usd_foil' : cards[4],
                        'euro' : cards[5],
                        'euro_foil' : cards[6],
                        'tix' : cards[7],
                    }
                    }
                )
            return price_data_single_day


@router.get("/{set}/{id}", description="Get the price data for one card. Last 25 results only.")
async def get_single_card_data(set: str, id: str, max: Union[int, None] = 25):
    if max > 25:
        # TODO: Figure out how to know where the > 25 query came from.
        log.error("User attempted to search more than 25 queries, setting to 25.")
        max = 25

    conn, cur = to_database.connect()
    cur.execute(""" 
        
        SELECT 
            card_info.info.name,
            card_info.sets.set_full,
            card_info.info.id,
            date,
            usd,
            usd_foil,
            euro,
            euro_foil,
            tix
        FROM card_data
        JOIN card_info.info
            ON card_data.set = card_info.info.set
            AND card_data.id = card_info.info.id
        JOIN card_info.sets
            ON card_data.set = card_info.sets.set
        WHERE
            card_data.set = %s AND card_data.id = %s

        """,

        (set, id)
        )
    
    result = cur.fetchall()
    price_data_single_card = {}
    if result == []:
        raise HTTPException(status_code=404, detail="This card does not exist on the database!")
    else:
        price_data_single_card = {
                "name": result[0][0],
                "set": result[0][2],
                "collector_id": result[0][1]
            }
        price_data_single_card["price_history"] = []
        for data in result[:max]:
            data = data[3:]
            price_data_single_card['price_history'].append(
                {
                    "date": data[0],
                    "usd" : data[1],
                    "usd_foil" : data[2],
                    "euro" : data[3],
                    "euro_foil": data[4],
                    "tix": data[5],
                }
            )
        log.debug(f"Returning card data for {price_data_single_card['name']}")
        return price_data_single_card

