from fastapi import APIRouter
from api_files.routers.internal.inventory_scripts import add_inventory
import logging
log = logging.getLogger()


router = APIRouter(
    prefix="/inventory",
    tags=["Manage your Inventory"],
)
router.include_router(add_inventory.router)