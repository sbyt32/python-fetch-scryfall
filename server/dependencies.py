# from fastapi import Response, status
from fastapi import Header, HTTPException
from scripts.config_reader import config_reader
import logging
log = logging.getLogger()
config = config_reader()

#  = Header() makes it so it has to pass through a header rather than a string
# ? All routes.

async def select_access(select_access: str = Header()):
    if select_access != config['CONNECT']['write_token']:
        log.error("Recieved incorrect or no select_access token.")
        raise HTTPException(status_code=403, detail="Incorrect or no provided select_access token")

# ? Admin route.

async def write_access(write_access: str = Header()):
    if write_access != config['CONNECT']['write_token']:
        log.error("Recieved incorrect or no read_access token.")
        raise HTTPException(status_code=400, detail="Incorrect or no provided read_access token")

# ?  Price route.

async def price_access(price_access: str = Header()):
    if price_access != config['CONNECT']['price_token']:
        log.error("Recieved incorrect or no price_access token.")
        raise HTTPException(status_code=403, detail="Incorrect or no provided price_access token")
