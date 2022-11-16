import requests
import logging
log = logging.getLogger()

def send_response(url:str):
    r = requests.get(url)
    if not r.ok:
        # todo: Add logging issue
        log.error(f"Request failed! Status code:{r.status_code}")
        # return r.json()
        # raise 
    else:
        card_list = r.json()
        # if card_list['object'] == 'error':
        #     return card_list
        return card_list
