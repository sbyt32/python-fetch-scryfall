from fastapi import APIRouter, Depends
from dependencies import price_access
from exceptions import RootException
from routers.pretty import PrettyJSONResp
router = APIRouter(
    prefix="/sales",
    dependencies=[Depends(price_access)],
    tags=["Fetch recent sale data from TCGP"]
)

@router.get("/", status_code=400, response_class=PrettyJSONResp)
async def root_access():
    raise RootException

# @router.get()