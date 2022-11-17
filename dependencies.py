# from fastapi import Response, status
from fastapi import Header, HTTPException
from fastapi.exceptions import RequestValidationError
from exceptions import TokenError
from scripts.config_reader import config_reader
import logging
log = logging.getLogger()
config = config_reader()

#  = Header() makes it so it has to pass through a header rather than a string

# ? All routes.
async def select_access(access: str):
    if access != config['CONNECT']['sec_token']:
        raise TokenError("access")


# ? Admin route.
async def write_access(write_access: str = Header()):
    if write_access != config['CONNECT']['write_token']:
        raise TokenError('write')


# ?  Price route.
async def price_access(price_access: str = Header()):
    if price_access != config['CONNECT']['price_token']:
        raise TokenError('price')
