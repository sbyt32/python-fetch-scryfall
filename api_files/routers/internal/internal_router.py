from api_files.dependencies import write_access
from fastapi import APIRouter, Depends
from api_files.routers.internal.card_tracking_scripts import _router_tracking
from api_files.routers.internal.group_scripts import _router_groups
from api_files.routers.internal.inventory_scripts import _router_inventory

router = APIRouter(    
    dependencies=[Depends(write_access)]
)
router.include_router(_router_tracking.router)
router.include_router(_router_groups.router)
router.include_router(_router_inventory.router)