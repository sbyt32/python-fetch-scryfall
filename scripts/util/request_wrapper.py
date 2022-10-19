import requests

def send_response(url:str):
    r = requests.get(url)
    if not r.ok:
        pass
    else:
        card_list = r.json()
        if card_list['object'] == 'error':
            pass # ? https://scryfall.com/docs/api/errors Maybe look at the warnings?
        return
        pass