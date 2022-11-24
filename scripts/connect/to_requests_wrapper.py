import requests
import logging
log = logging.getLogger()

def send_response(method:str, url:str, **kwargs):
    r = requests.request(method, url, **kwargs)
    if not r.ok:
        # todo: Add logging issue
        log.error(f"Request failed! Status code:{r.status_code}")
        # return r.json()
        # raise 
    else:
        card_list = r.json()
        return card_list
