from fastapi import APIRouter
from api_files.routers.internal.group_scripts import add_groups, remove_groups
import logging
log = logging.getLogger()


router = APIRouter(
    prefix="/groups",
    tags=["Manage your card groupings"],
)
router.include_router(add_groups.router)
router.include_router(remove_groups.router)