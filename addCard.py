import json
import ndjson
import os 
import requests
from pick import pick

cardsAdded = []

# Get list of sets from a single card
def cardSearchSetList(cardName, searchTitle):
    r = requests.get('https://api.scryfall.com/cards/search?q={}&unique=prints'.format(cardName))
    setList = r.json()
    option = []
    for x in setList['data']:
        option.append([x['name'], x['set_name'], x['collector_number'], x['set_name'] + '  ||  Set # ' + x['collector_number']])
    selected, index = pick([i[3] for i in option], searchTitle, '>>')
    # Replace the last bit with the link, and the first with the set code
    option[index][-1] = setList['data'][index]['uri']
    option[index][1] = setList['data'][index]['set']
    selected = option[index]

    # Merge the information together before writing to ./cards.json
    cardInfo =["name","set", "id", "uri"]
    cardToStore = dict(zip(cardInfo,selected))

    # Double Check if the card does not already exist on the search.
    with open('./cards.ndjson') as cardRead:
        duplicateCard = False
        reader = ndjson.load(cardRead)
        for card in reader:
            if card == cardToStore:
                duplicateCard = True
                print('Dupes!')
                break
        if duplicateCard == True:
            repeatSearch = pick(["Yes", "No"], "{} ({}) is already being tracked!\nIs there another card you want to track?".format(cardToStore['name'], cardToStore['set'].upper()), ">>")
            if repeatSearch[0] == "Yes":
                cardSearch()
            elif len(cardsAdded) >= 1:
                appendCard(None)
            elif len(cardsAdded) == 0 and repeatSearch[0] == "No":
                print('No cards were added!')
        else:
            appendCard(cardToStore)

def appendCard(cardToStore):
    if cardToStore != None:
        with open('./cards.ndjson', 'a') as cardDatabase:
            cardDatabase.write(json.dumps(cardToStore)+'\n')
        repeatSearch = pick(["Yes", "No"], "{} ({}) has been added to track!\nIs there another card you want to track?".format(cardToStore['name'], cardToStore['set'].upper()), ">>")
        cardsAdded.append(cardToStore['name'])

    if repeatSearch[1] == 0:
        cardSearch()
    else:
        if len(cardsAdded) > 1:
            print("The following has been added:\n")
            for card in cardsAdded:
                print('{}'.format(card))
            print("\nDon't forget to query the prices!")
        else:
            print("{} has been added to track!\nDon't forget to query the price!".format(cardToStore['name']))


# Find the card!
def cardSearchList(cardList, cardToSearch):
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
    # Clean loops
    os.system('cls')
    cardToSearch = ""
    cardToSearch = input("Hello! What card are you looking to add? ")
    if cardToSearch != "":
        r = requests.get('https://api.scryfall.com/cards/search?q={}&pretty=true'.format(cardToSearch))
        cardList = r.json()
        if cardList['object'] == 'error':
            print('There is no results for {}, please try again!'.format(cardToSearch))
        else:
            cardSearchList(cardList, cardToSearch)
    else:
        print("Hey! You can't send empty values!")

# ? I wish there was an easier way to make this not work backwords???
cardSearch()