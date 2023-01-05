from api_files.routers.data.inventory_scripts import return_inventory
from fastapi import APIRouter, Depends, HTTPException, Response, status
from api_files.dependencies import select_access
from api_files.response_models.card_info import CardInfo
from api_files.response_class.pretty import PrettyJSONResp
import scripts.connect.to_database as to_db

router = APIRouter(
    prefix="/inventory",
    tags=["Manage your Inventory"],
    dependencies=[Depends(select_access)]
)

router.include_router(return_inventory.router)