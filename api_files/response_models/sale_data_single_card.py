from pydantic import BaseModel
import datetime


class SaleData(BaseModel):
    order_date: datetime.datetime
    condition : str
    variant   : str
    quantity  : int
    buy_price : int
    ship_price: int

class CardInfo(BaseModel):
    "Internal"
    card_name: str
    set_name: str
    tcg_id: str
    sale_data: list[SaleData]

class SaleDataSingleCardResponse(BaseModel):
    resp  : str
    response: int
    data: list[CardInfo]