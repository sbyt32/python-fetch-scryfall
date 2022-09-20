from time import sleep
import ndjson
import os
import requests
import csv
import pathlib
# For Date
import datetime
fetchedTime = datetime.datetime.now()


with open('./cards.ndjson', 'r') as cardDatabase:
    reader = ndjson.reader(cardDatabase)
    for card in reader:
        # making it more cohesive later
        cardSet = card['set']
        cardName = card['name']
        cardID = card['id']
        filePath = "./Tracking/{}/{}_{}.csv".format(cardSet,cardID,cardName.lower()[slice(7)])
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
                print('Now tracking: {} from {}!'.format(cardName, cardSet.upper()))
            elif fetchedTime.timestamp() - epochTime < 86400: 
                print('It is too soon to update! Check back tomorrow!')
                sleep(.2)
                continue # goes back.
            else:
                print('Updating: {} from {}...'.format(cardName,cardSet.upper()))
            writer.writerow(toParse)                
        # To not overload the API
        sleep(.2)