from api_files.routers.data.card_tracking_scripts import _router_tracking
from api_files.routers.data.inventory_scripts import _router_inventory
from api_files.routers.data.price_data_scripts import _router_sales
from fastapi import Depends, APIRouter, Response, status
from api_files.dependencies import select_access


router = APIRouter(
    dependencies=[Depends(select_access)]
)

router.include_router(_router_tracking.router)
router.include_router(_router_inventory.router)
router.include_router(_router_sales.router)