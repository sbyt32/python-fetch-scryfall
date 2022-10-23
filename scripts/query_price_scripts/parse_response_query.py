import csv
import arrow
# local = 

# print(arrow.utcnow().format('MM-DD-YY'))

def append_cards(r:list, path:str):
    usd         =   r['usd']
    usd_foil    =   r['usd_foil']
    eur         =   r['eur']
    eur_foil    =   r['eur_foil']
    mtgo        =   r['tix']

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
        pass # TODO: Here should the check if it's less than 24hr
             # ? May not be nessecary, if running through crontab?

    
             