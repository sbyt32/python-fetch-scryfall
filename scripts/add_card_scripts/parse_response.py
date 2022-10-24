from pick import pick

def parse_list(list:dict):
    list_qty = list['total_cards']

    # * Check if returned more than one result.
    if list_qty == 1:
        return list['data'][0]['name']

    elif list_qty > 1:
        options = []
        
        for cards in list['data']:
            if 'paper' in cards['games']:
                # * Parse only the cards that exist in physical form
                options.append(cards)
        select = pick([i['name'] for i in options])

        return select[0]
    else:
        pass # ! Error, in case that it gives me something that has ZERO cards (idk if possible)
             # ? Would this not give a 400 error, if the case?