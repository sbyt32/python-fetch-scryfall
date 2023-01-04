from fastapi import APIRouter
from api_files.routers.data.group_scripts import return_groups
router = APIRouter(
    prefix="/groups",
    tags=['Card Groups']
)

router.include_router(return_groups.router)