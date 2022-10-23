import scripts

def add_card():
    query = input('What to Search? ')
    r = scripts.send_response(f'https://api.scryfall.com/cards/search?q={query}')
    list = scripts.parse_list(r)
    print(list)
    