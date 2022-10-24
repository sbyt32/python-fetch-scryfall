import requests
from pick import pick

def select_card(query:str):
    r = requests.get(f'https://api.scryfall.com/cards/search?q=%21"{query}"+include%3Aextras&unique=prints')
    resp_list = r.json()
    options = []
    for cards in resp_list['data']:
        if 'paper' in cards['games']:
            identify_string = f"{cards['set_name']:40} | {cards['collector_number']}"
            options.append([identify_string, cards])

    # ? x is a filler here, to primarily get the location. We do not care about the actual text they picked.
    x, i = pick([i[0] for i in options], f'{"":2}{"Set":40} | Collector Number')
    select = options[i][1]
    # TODO: For loop, decide which option to select. resp_list['data']
    card_info = [
        "name", # Name of the Card
        "set",  # Set Name
        "id",   # The card ID in the set, this is important
        "uri"   # The link that directly pulls the card you want.
    ]
    card_details = [select['name'], select['set'], select['collector_number'], select['uri']]
    return dict(zip(card_info, card_details))
    # for 

        # Get the information, return a result that passes on the information.
    pass