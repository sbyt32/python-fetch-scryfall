# for date
import datetime
time = datetime.datetime.now()

import requests
r = requests.get('https://api.scryfall.com/cards/a9738cda-adb1-47fb-9f4c-ecd930228c4d?format=json&pretty=true')
card = r.json()
cardNamePath = card['name']
filePath = "./{}/{}_{}.csv".format(card['set'], card['collector_number'], cardNamePath.lower()[slice(7)])
    # ./[set]/[collector number] [cardname]

import csv
with open(filePath, 'a', newline='') as cardDatabase:
    # TODO: Check if last check was less than a day 

    writer = csv.writer(cardDatabase, quoting=csv.QUOTE_MINIMAL)
    # toParse = [{time}, [card['prices']['usd']]]
    toParse = [
        time, card['prices']['usd']
    ]

    writer.writerow(toParse)
    # ! Fix the fact that it goes onto the same column and not the next one 
    # writer.writerow([time])
    # writer.writerow([card['prices']['usd']])