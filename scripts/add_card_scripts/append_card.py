import json
import os
import ndjson


def append_query(query:str):
    if not os.path.exists('data/cards_to_query.ndjson'):
        os.makedirs('data/cards_to_query.ndjson')

    # * Open the ndjson file.
    with open('data/cards_to_query.ndjson') as cards_database:
        reader = ndjson.load(cards_database)
        cards_database.close()
    duplicate = False


    for card in reader:
        if card == query:
            duplicate = True
            break
    if duplicate:
        pass # TODO: This needs to see if the content is already there
    else:

        if query is not None:
            with open('data/cards.ndjson', 'a') as cards_to_write:
                cards_to_write.write(ndjson.dumps(query) + '\n')
            pass # Here is where repeat search would be
                 # ? Should I put that as a separate script?