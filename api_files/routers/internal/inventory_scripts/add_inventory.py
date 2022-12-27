from fastapi import APIRouter
from api_files.request_models.add_inventory_model import AddInventory
from psycopg.rows import dict_row
import psycopg
import scripts.connect.to_database as to_db
import scripts.connect.to_requests_wrapper as to_requests_wrapper
import logging
log = logging.getLogger()

router = APIRouter()

@router.post("/add")
async def add_card_groups_with_set_id(inventory: AddInventory):
    if inventory.set and inventory.col_num and not inventory.tcg_id:
        resp = to_requests_wrapper.send_response("GET", f'https://api.scryfall.com/cards/{inventory.set.lower()}/{inventory.col_num.lower()}')
        if inventory.card_variant == "Etched":
            inventory.tcg_id = resp['tcgplayer_etched_id']
        else:
            inventory.tcg_id = str(resp['tcgplayer_id'])
        
    if inventory.tcg_id:
        conn, cur = to_db.connect_db(row_factory = dict_row)

        cur.execute("""
            SELECT 
                EXISTS (
                    SELECT 1 
                    FROM inventory
                    WHERE tcg_id        = %s 
                    AND card_condition  = %s 
                    AND card_variant    = %s 
                    AND buy_price       = %s
                )
            """, (      
                    inventory.tcg_id,
                    inventory.condition,
                    inventory.card_variant,
                    inventory.buy_price
                )
        )

        if cur.fetchone()['exists']:
            cur.execute("""
                UPDATE inventory
                SET qty = inventory.qty + %s
                WHERE tcg_id = %s
                AND card_condition = %s
                AND card_variant = %s
                AND buy_price = %s
                """, (
                    inventory.qty,
                    inventory.tcg_id,
                    inventory.condition,
                    inventory.card_variant,
                    inventory.buy_price
                    )
            )
        else:
            cur.execute("""
                INSERT INTO inventory
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """, (
                    inventory.tcg_id,
                    inventory.qty,
                    inventory.buy_price,
                    inventory.condition,
                    inventory.card_variant
                    )
            )

        cur.execute("""
            SELECT * FROM inventory 
            WHERE 
                tcg_id = %s 
                AND card_condition = %s 
                AND card_variant = %s
                AND buy_price = %s
            """, (
                inventory.tcg_id, 
                inventory.condition, 
                inventory.card_variant,
                inventory.buy_price
                )
        )
        inventory_check = cur.fetchone()
        conn.commit()
        return inventory_check