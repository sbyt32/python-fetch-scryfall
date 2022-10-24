import scripts

def add_card():
    query = input('What to Search? ')
    r = scripts.util_send_response(f'https://api.scryfall.com/cards/search?q={query}')
    list = scripts.add_parse_list(r)
    selection = scripts.add_select_card(list)
    scripts.add_append_query(selection)
    