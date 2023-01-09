from fastapi import APIRouter, Depends, HTTPException, Response, status
from api_files.dependencies import select_access
from api_files.response_models.card_info import CardInfo
from psycopg.rows import dict_row
import scripts.connect.to_database as to_db

router = APIRouter()

@router.get(
    path="/",
    description="Return your entire inventory."
)

async def get_inventory():
    conn, cur = to_db.connect_db(row_factory = dict_row)

    cur.execute("""
        SELECT
            info.name "Name",
            set.set_full "Set",
            SUM(inventory.qty) "Quantity",
            inventory.card_condition "Condition",
            inventory.card_variant "Variation",
            TRUNC(AVG(avg_price.total_qty) / SUM(inventory.qty),2) as "Avg. Cost"
        FROM inventory as inventory
        JOIN card_info.info as info
            ON info.tcg_id = inventory.tcg_id
        JOIN card_info.sets as set
            ON info.set = set.set
        JOIN (
            SELECT 
                inventory.tcg_id,
                SUM (inventory.qty * inventory.buy_price)::numeric AS total_qty,
                inventory.card_condition,
                inventory.card_variant
            FROM inventory 
            GROUP BY
                inventory.tcg_id,
                inventory.card_condition,
                inventory.card_variant
        ) AS avg_price
            ON avg_price.tcg_id = inventory.tcg_id
            AND avg_price.card_condition = inventory.card_condition
            AND avg_price.card_variant = inventory.card_variant
        GROUP BY
            info.name,
            set.set_full,
            inventory.card_condition,
            inventory.card_variant
    """)

    return cur.fetchall()