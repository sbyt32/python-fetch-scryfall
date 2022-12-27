from typing import Union
from pydantic import BaseModel

class AddInventory(BaseModel):
    tcg_id      : Union[str, None] = None
    set         : Union[str, None] = None
    col_num     : Union[str, None] = None
    qty         : int
    buy_price   : int
    condition   : str
    card_variant: str

