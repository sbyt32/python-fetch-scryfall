import scripts as scripts

def add_card():
    query = input('What to Search? Type "quit" to exit. ')
    if query != "quit":
        r = scripts.send_response(f'https://api.scryfall.com/cards/search?q={query}')
        list = scripts.add_parse_list(r)
        selection = scripts.add_select_card(list)
        scripts.add_append_query(selection)
    else:
        print('Exiting script!')