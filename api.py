import os
from fastapi import Depends, FastAPI, Response, status
from exceptions import frank_exception, frank_exception_handler
from dependencies import write_access, select_access
from routers import return_card_info, return_price_info
from routers.internal import admin
# Logging Information
import logging
# ? For some reason, scripts/config_reader.py having the logging setup works fine. Need to know why eventually. Commented out for now
# import logging_details
# logging_details.log_setup()
log = logging.getLogger()
log.setLevel(logging.INFO)

# * Accessing the database should require the select_access token
app = FastAPI(dependencies=[Depends(select_access)])
app.include_router(return_card_info.router)
app.include_router(return_price_info.router)
app.include_router(admin.router)

@app.get("/", status_code=200, tags=["Test Connection"])
async def root(response: Response):
    if os.path.exists('config.ini'):
        raise frank_exception
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'resp'  :   'error',
            'status':   response.status_code,
            'detail':   'Configuration file does not exist. Script will not function.'
        }

app.add_exception_handler(frank_exception, frank_exception_handler)
