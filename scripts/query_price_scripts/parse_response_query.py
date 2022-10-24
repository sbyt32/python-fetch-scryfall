import csv
import arrow
import os 
# local = 

# print(arrow.utcnow().format('MM-DD-YY'))

def append_cards(r:list, path:str):
    usd         =   r['prices']['usd']
    usd_foil    =   r['prices']['usd_foil']
    eur         =   r['prices']['eur']
    eur_foil    =   r['prices']['eur_foil']
    mtgo        =   r['prices']['tix']

    if not os.path.exists(path):
        with open(path, 'a', newline='') as card_write_to_csv:
            writer = csv.writer(card_write_to_csv, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['DATE', 'USD', 'USD_FOIL', 'EURO', 'EURO_FOIL', 'TIX'])

    with open(path, 'a', newline='') as card_write_to_csv:
        writer = csv.writer(card_write_to_csv, quoting=csv.QUOTE_MINIMAL)
        to_parse = [
            arrow.utcnow().format('MM-DD-YY'),
            usd,
            usd_foil,
            eur,
            eur_foil,
            mtgo
        ]
        writer.writerow(to_parse)
        card_write_to_csv.close()
        # TODO: Here should the check if it's less than 24hr
        # ? May not be nessecary, if running through crontab?

    
             