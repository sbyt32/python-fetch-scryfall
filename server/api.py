import os
from fastapi import Depends, FastAPI, Response, HTTPException, status
from dependencies import write_access, select_access
from routers import card, price
from internal import admin
# Logging Information
import logging
import logging_details
logging_details.log_setup()
log = logging.getLogger()
log.setLevel(logging.INFO)


# * Accessing the database should require the select_access token
app = FastAPI(dependencies=[Depends(select_access)])

app.include_router(card.router)
app.include_router(price.router)
app.include_router(
    admin.router,
    prefix="/admin",
    dependencies=[Depends(write_access)],
    responses={418: {"description": "I'm a teapot"}}
)


@app.get("/", status_code=200)
async def root(response: Response):
    if os.path.exists('config.ini'):
        raise HTTPException(status_code=400, detail="Buddy, this ain't the right way to get the cards.")
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'resp'  :   'error',
            'status':   response.status_code,
            'detail':   'Configuration file does not exist. Script will not function.'
        }