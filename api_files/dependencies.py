# from fastapi import Response, status
from fastapi import Header
from api_files.exceptions import TokenError
from scripts.config_reader import config_reader
import logging
log = logging.getLogger()
config = config_reader("CONNECT", "tokens")

#  = Header() makes it so it has to pass through a header rather than a string

# ? All routes.
async def select_access(access: str):
    if access != config['sec_token']:
        raise TokenError("access")


# ? Admin route.
async def write_access(write_access: str = Header()):
    if write_access != config['write_token']:
        raise TokenError('write')


# ?  Price route.
async def price_access(price_access: str = Header()):
    if price_access != config['price_token']:
        raise TokenError('price')
