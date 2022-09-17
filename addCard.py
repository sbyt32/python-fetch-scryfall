import json
import os 
import requests
from pick import pick
# https://api.scryfall.com/cards/search?q=
# https://api.scryfall.com/cards/search?q=${card}&unique=prints

addCards = True
os.system('cls')

cardToSearch = input("Hello! What card are you looking to add? ")


# Get list of sets from a single card
def cardSearchSetList(cardName, searchTitle):
    print(cardName)
    r = requests.get('https://api.scryfall.com/cards/search?q={}&unique=prints'.format(cardName))
    setList = r.json()
    option = []
    for x in setList['data']:
        option.append([x['set_name'], x['collector_number'], x['set_name'] + '  ||  Set # ' + x['collector_number']])
    selected, index = pick([i[2] for i in option], searchTitle, '>>')
    option[index][-1] = setList['data'][index]['uri']
    selected = option[index]
    # TODO: Write these results to cards.json or something?
    print(selected)

# Find the card!
def cardSearchList(cardList):
    listQty = cardList['total_cards']
    if listQty == 1:
        cardSearchSetList(cardList['data'][0]['name'], 'Wow, there is exactly one result for {}. Which set are you looking for?'.format(cardToSearch))
    elif listQty > 1:
        option = []
        for x in cardList['data']:
            option.append(x['name'])
        selected = pick(option, "Wow, more than 1! Which card are you looking for?", '>>')
        cardSearchSetList(selected[0], searchTitle="Which set would you like to track?")
    else:
        print('Error???')

# Search what you want!
def cardSearch():
    if cardToSearch is not "":
        r = requests.get('https://api.scryfall.com/cards/search?q={}&pretty=true'.format(cardToSearch))
        cardList = r.json()
        cardSearchList(cardList)
    else:
        print("Hey! You can't send empty values!")

# ? I wish there was an easier way to make this not work backwords???
cardSearch()
