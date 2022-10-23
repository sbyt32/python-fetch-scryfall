import requests

def select_card(query:str):
    r = requests.get(f'https://api.scryfall.com/cards/search?q=%21"{query}"+include%3Aextras&unique=prints')
    resp_list = r.json()
    # TODO: For loop, decide which option to select. resp_list['data']
    card_info = [
        "name", # Name of the Card
        "set",  # Set Name
        "id",   # The card ID in the set, this is important
        "uri"   # The link that directly pulls the card you want.
    ]

    # for 

        # Get the information, return a result that passes on the information.
    pass