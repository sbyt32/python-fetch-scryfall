import scripts.connect.to_database as to_db
from fastapi import APIRouter, Depends
from api_files.dependencies import price_access
from api_files.exceptions import RootException
from api_files.routers.pretty import PrettyJSONResp

router = APIRouter(
    prefix="/sales",
    dependencies=[Depends(price_access)],
    tags=["Fetch recent sale data from TCGP"]
)

@router.get("/", status_code=400, response_class=PrettyJSONResp)
async def root_access():
    raise RootException

@router.get("/card/{tcg_id}", description="Get the most recent sales from this card. Updates every week")
async def filler_name(tcg_id:str):
    cur = to_db.connect_db()[1]

    cur.execute("""
        SELECT 
            card_info.info.name,
            card_info.sets.set_full,
            order_date,
            condition,
            variant,
            qty,
            buy_price,
            ship_price
        FROM 
            card_data_tcg_copy 
        JOIN card_info.info
            ON card_data_tcg_copy.tcg_id = card_info.info.tcg_id
        JOIN card_info.sets
            ON card_info.info.set = card_info.sets.set
        WHERE 
            card_data_tcg_copy.tcg_id = %s
        ORDER BY
            order_date asc
        LIMIT '25';
    """, (tcg_id,))
    
    result = cur.fetchall()
    if result == []:
        raise Exception
    else:
        sale_data_single_card = {
        "name": result[0][0],
        "tcg_id": tcg_id,
        "set"   : result[0][1]
        }
        sale_data_single_card['sale_data'] = []
        for data in result:
            data = data[2:]
            sale_data_single_card['sale_data'].append(
                {
                    "order_date":data[0], 
                    "condition":data[1],
                    "variant":data[2],
                    "quantity":data[3],
                    "buy_price":data[4],
                    "ship price":data[5]
                }
            )
        return sale_data_single_card