from pydantic import BaseModel

class CardInfo(BaseModel):
    resp  : str
    status: int
    data: list