from api_files.routers.data.card_tracking_scripts import return_card_info
from fastapi import APIRouter, Depends, HTTPException, Response, status
from api_files.dependencies import select_access
from api_files.response_models.card_info import CardInfo
from api_files.response_class.pretty import PrettyJSONResp
import scripts.connect.to_database as to_db

router = APIRouter(
    prefix="/card",
    tags=["Get some card info"],
    dependencies=[Depends(select_access)],
    responses={404: {"description": "Not found"}},
)

router.include_router(return_card_info.router)
