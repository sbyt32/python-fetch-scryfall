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

# @router.get()