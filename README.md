# MTG Price Fetcher
> A simple price fetcher for Magic: The Gathering, powered via Scryfall's API and written in Python.

## How it works
___
`fetcher.py` will, at the moment, prompt you to track a card, searchable by name. That information is then stored in `data/cards_to_query.ndjson`, which is called by the next script. It will pull the information and acquire the price data via Scryfall, which will be put into `data/tracking/SET/NUMBER_CARDNAME.csv`. 

## Packages
___
    arrow
    ndjson
    requests
    pick