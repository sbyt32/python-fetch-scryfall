from time import sleep
import ndjson
import os
import requests
import csv
import pathlib
import re
# For Date
import datetime
fetchedTime = datetime.datetime.now()

def sanitizeString(name):
    name = re.sub("[',]","",name)
    name = re.sub("['\s]","_", name)
    name = name.lower()[slice(9)]
    if re.search("$_",name):
        name = name.rstrip(name[-1])
    return name
        

def checkSetPromo(set,id):
    if re.search("^p", set) and len(set) == 4:
        set = set.upper()
        if re.search("$s", id):
            return f"{set} (Date-stamped Promo)"
        elif re.search("$a",id):
            return f"{set} (Ampersand Promo)"
        else:
            return f"{set} (Planeswalker-stamped Promo)"
    else:
        return f"{set.upper()}"

with open('./cards.ndjson', 'r') as cardDatabase:
    reader = ndjson.reader(cardDatabase)
    for card in reader:
        # making it more cohesive later
        cardSet = card['set']
        cardID = card['id']
        cardName = card['name']
        filePath = "./Tracking/{}/{}_{}.csv".format(cardSet,cardID,sanitizeString(cardName))
        # Creating a directory if does not exist
        if not os.path.exists('./Tracking/{}'.format(cardSet)):
            print('Making the directory: {}'.format(cardSet))            
            os.makedirs('./Tracking/{}'.format(cardSet))
        # Fetching the info from scryfall
        r = requests.get(card['uri'])
        cardSearched = r.json()
        # Updating all the information, also makes file if does not exist
        with open(filePath, 'a', newline='') as cardToCSV:
            writer = csv.writer(cardToCSV, quoting=csv.QUOTE_MINIMAL)
            # TODO: Add support for EURO and TIX
            toParse = [fetchedTime, cardSearched['prices']['usd']]
            # Time check, don't update if less than a day
            epochTime = pathlib.Path(filePath).stat().st_mtime
            if fetchedTime.timestamp() - epochTime < 5:
                print('Now tracking: {} from {}!'.format(cardName, checkSetPromo(cardSet,cardID)))
            elif fetchedTime.timestamp() - epochTime < 86400: 
                print('It is too soon to update! Check back tomorrow!')
                sleep(.2)
                continue # goes back to start of loop.
            else:
                print('Updating: {} from {}...'.format(cardName, checkSetPromo(cardSet,cardID)))
            writer.writerow(toParse)                
        # To not overload the API
        sleep(.2)