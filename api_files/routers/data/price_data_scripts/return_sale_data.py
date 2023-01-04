import scripts.connect.to_database as to_db
from fastapi import APIRouter, Depends, Response, status
from psycopg.rows import dict_row
from api_files.exceptions import RootException

router = APIRouter(
    prefix="/sales",
)

@router.get("/", status_code=400)
async def root_access():
    raise RootException

@router.get("/card/{tcg_id}", description="Get the most recent sales from this card. Updates every week")
async def get_tcg_sales(tcg_id:str, response: Response):
    cur = to_db.connect_db(row_factory = dict_row)[1]

    cur.execute("""
        SELECT
            info.name "card_name",
            sets.set_full "set_name",
            info.tcg_id 
        FROM card_info.info AS info
        JOIN card_info.sets AS sets
            ON info.set = sets.set
        WHERE
            info.tcg_id = %s
    """, (tcg_id,))

    searched_card = cur.fetchone()

    if searched_card:

        cur.execute("""
            SELECT 
                order_date,
                condition,
                variant,
                qty "quantity",
                buy_price,
                ship_price
            FROM 
                card_data_tcg
            JOIN card_info.info
                ON card_data_tcg.tcg_id = card_info.info.tcg_id
            JOIN card_info.sets
                ON card_info.info.set = card_info.sets.set
            WHERE 
                card_data_tcg.tcg_id = %s
            ORDER BY
                order_date desc
            LIMIT '5'
        """, (tcg_id,))
        
        recieved_sale_data = cur.fetchall()


        searched_card['sale_data'] = recieved_sale_data
        response.status_code = status.HTTP_200_OK

        return {
            "resp": "hello",
            "status": response.status_code,
            "data": [searched_card]
        }
