# MTG Price Fetcher
> A simple price fetcher for Magic: The Gathering, powered via Scryfall's API and written in Python.

## How it works
<!-- `fetcher.py` will, at the moment, prompt you to track a card, searchable by name. That information is then stored in `data/cards_to_query.ndjson`, which is called by the next script. It will pull the information and acquire the price data via Scryfall, which will be put into `data/tracking/SET/NUMBER_CARDNAME.csv`.  -->
Script is divided into groups, `local` and `server`. Place the `server` on your server and `local` on the computer / etc.
### Local
`config_setup.py` prompts you for information to pass to the rest of the scripts.
- Host      (Default: localhost)
- User      
- Password  
- Database  (Default: price_tracker)

If you need to change information, such as to change databases, rerun the script.

`main.py` fetches the card data from Scryfall, searching by card name. It divides them based on each set, using Scryfall's organization system. [For more information, click here](https://scryfall.com/sets). It will create the database specified in `config_setup.py`; it is assumed that said database does not exist, however it should function as normal. 

`config_setup.py` should be ran first, before `main.py`. Otherwise, the script **will** fail. 
### Server
`config_setup.py` functions the exact same way as it does for its `local` counterpart. 
- Host      (Default: localhost)
- User      
- Password  
- Database  (Default: price_tracker)
- Database existance (Default: Yes)

It is assumed that `local/config_setup.py` and `local/main.py` has been ran at least once, otherwise no information will be parsed and the database won't be set up correctly.

`fetcher.py` pulls info from the database, grabbing the URL for that card on Scryfall. It will then place the data prices for both US and EU markets, powered respectively by TCGPlayer and MagicCardMarket, into a PostgreSQL database.

If there is legacy data, `fetcher.py` will transform the data and place it into the PostgreSQL database. If that is the case, please rerun the script as it will not fetch the information for today otherwise. 

## Packages
    arrow
    ndjson
    requests
    pick
    psycopg2-binary