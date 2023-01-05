from pydantic import BaseModel

# * https://fastapi.tiangolo.com/tutorial/body/#__tabbed_2_1
class CardGroups(BaseModel):
    set: str
    id: str
    group: str
