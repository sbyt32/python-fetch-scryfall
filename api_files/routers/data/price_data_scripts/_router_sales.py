from api_files.routers.data.price_data_scripts import  return_sale_data, return_price_info
from fastapi import APIRouter, Depends
from api_files.dependencies import price_access

router = APIRouter(
    dependencies=[Depends(price_access)],
    tags=["Fetch card prices"]
)

router.include_router(return_sale_data.router)
router.include_router(return_price_info.router)