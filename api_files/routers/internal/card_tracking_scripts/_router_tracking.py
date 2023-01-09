from fastapi import APIRouter
from api_files.routers.internal.card_tracking_scripts import track_by_tcg, track_by_set_id, track_by_sf
import logging
log = logging.getLogger()


router = APIRouter(    
    tags=["Manage price-tracked cards"],)
router.include_router(track_by_set_id.router)
router.include_router(track_by_sf.router)

# TODO:
# router.include_router(track_by_tcg.router)