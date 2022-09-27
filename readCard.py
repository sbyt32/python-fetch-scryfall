import os
from sanitizeString import sanitizeString
import ndjson
import csv
from tabulate import tabulate
from pick import pick
headers = ["Date", "USD", "USD (Foil)", "EUR", "EUR (Foil)", "Tickets"]
title = "Card Lookup"
cardSearch = None
os.system('cls')
with open('./cards.ndjson', 'r') as cardDatabase:
    reader = ndjson.reader(cardDatabase)
    # sortType = pick(["Name", "Set", "Search"], f"{title}\nHow would you like to search?")
    sortType = pick(["Name", "Set"], f"{title}\nHow would you like to search?")

    # ! Add the "Search" to the Pick Above.
    if sortType[0] == "Search":
        cardSearch = input("What you looking for? ")
        # ! This whole thing here is fucked, fix later?
        while cardSearch:
            dataStorage = [card['name'] for card in reader]
            if cardSearch in dataStorage:
                print('found card!')
                break
    else:
        option = []
        for card in reader:
            # print(card)
            option.append([card['name'], card['set'], card['id']])
            # Set feature doesn't work if >1 card. 
            # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
        selected, index = pick([i[sortType[1]] for i in option])
        selected = option[index]
        cardName = selected[0]
        cardSet = selected[1]
        cardID = selected[2]

with open(f'./Tracking/{cardSet}/{cardID}_{sanitizeString(cardName)}.csv', 'r', newline='') as cardLookup:
    reader = csv.reader(cardLookup)
    dataList = []
    for x in reader:
        dataList.append(x)
    print(cardName)
    print(tabulate(dataList, headers, disable_numparse=True))

    # sortType = pick(["Name", "Set", "Search"], f"{title}\nHow would you like to search?")
    # if sortType[0] == "Search":
    #     sortType = ["Name",0]
    #     cardSearch = input("What card are you looking for? ")

    # dataStorage = [card[f'{sortType[0].lower()}'] for card in reader]
    # if cardSearch is None:
    #     cardChoice = pick(dataStorage, f"{title}\nSearching by: {sortType[0]}")
    # else:
    #     sortType = ['Name', 0]
    #     while cardSearch:
    #         if cardSearch in dataStorage:
    #             cardChoice = cardSearch
    #             cardDatabase.close()
    #             break
    #         else:
    #             searchAgain = pick(["Yes","No"], "No results\nWould you like to search again?")
    #             if searchAgain[0] == "No":
    #                 break
    #             cardSearch = input("What card are you looking for? ")