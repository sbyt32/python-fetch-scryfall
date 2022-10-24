import json
import os
import ndjson


def append_query(query:dict):
    card_path = 'data/cards_to_query.ndjson'
    if not os.path.exists(card_path):
        os.makedirs('data')
        open(card_path, 'x')


    with open(card_path) as card_database:
        cards_to_compare = ndjson.reader(card_database)          

        duplicate = False

        for card in cards_to_compare:
            if card == query:
                duplicate = True
                break

        if duplicate:
            return # TODO: This needs to see if the content is already there
        else:
            if query is not None:
                with open(card_path, 'a') as cards_to_write:
                    writer = ndjson.writer(cards_to_write)
                    writer.writerow(query)
                    # Here is where repeat search would be
                    # ? Should I put that as a separate script?