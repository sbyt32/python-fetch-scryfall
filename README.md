# MTG Price Fetcher
> A simple price fetcher for Magic: The Gathering, powered via Scryfall's API and written in Python.

## How it works
<!-- `fetcher.py` will, at the moment, prompt you to track a card, searchable by name. That information is then stored in `data/cards_to_query.ndjson`, which is called by the next script. It will pull the information and acquire the price data via Scryfall, which will be put into `data/tracking/SET/NUMBER_CARDNAME.csv`.  -->
Script is divided into groups, `local` and `server`. Place the `server` on your server and `local` on the computer / etc.

<!-- TODO: Update This -->
<!-- ### Local
`config_setup.py` prompts you for information to pass to the rest of the scripts.
- Host      (Default: localhost)
- User      
- Password  
- Database  (Default: price_tracker)

If you need to change information, such as to change databases, rerun the script.

`main.py` fetches the card data from Scryfall, searching by card name. It divides them based on each set, using Scryfall's organization system. [For more information, click here](https://scryfall.com/sets). It will create the database specified in `config_setup.py`; it is assumed that said database does not exist, however it should function as normal. 

`config_setup.py` should be ran first, before `main.py`. Otherwise, the script **will** fail.  -->

### Server
`set_up.py` functions the exact same way as it does for its `local` counterpart. The information is stored in `config.ini`. Both scripts, `api.py` and `price_fetcher.py`, **WILL** fail without a `config.ini` file.

### config.ini

| Data               | Desc                                                                                          | Default (if any) |
|--------------------|-----------------------------------------------------------------------------------------------|------------------|
| Host               | Where to connect to for the database                                                          | localhost        |
| User               | Username for the PostgreSQL database                                                          |                  |
| Password           | Password for the user                                                                         |                  |
| Database           | The database name to store the pulled prices. The database does not have to exist to be valid | price_tracker    |
| Tokens             |                                                                                               |                  |
| - Access           | A token to access the entire database. Pass it through the headers                            |                  |
| - Write            | A token to add / remove card information. Be careful with it! Pass it through the headers     |                  |
| - Price            | A token to fetch price information. Pass it through the headers                               |                  |
| Database Existance | Boolean. If false: creates the database structure                                             | True             |
<!-- It is assumed that `local/config_setup.py` and `local/main.py` has been ran at least once, otherwise no information will be parsed and the database won't be set up correctly. -->

<!-- `fetcher.py` pulls the Scryfall URL of certain cards from the database and sends a request to the Scryfall API.  It will then parse the price data and insert it into the database, in the table `card_data`.  -->

`api.py` was created with [hypercorn](https://pgjones.gitlab.io/hypercorn/).

    hypercorn api:app

Information can, after running, be found in http://127.0.0.1:8000/docs.

<!-- If there is legacy data, `fetcher.py` will transform the data and place it into the PostgreSQL database. If that is the case, please rerun the script as it will not fetch the information for today otherwise.  -->
## Libraries
    arrow
    requests
    psycopg
    fastapi
    hypercorn

## TODO:
- Server
    - Add card grouos
    - Manipulate Price Data
    - Consistent import names
    - Committing as little as possible in the sale fetch data.
    - Separate script for updating sale data for cards after initial search.
- API
    - Refactor router-related data
    - Custom classes for response formats
- Both
    - Custom Exceptions for cleaner errors
    - Update README

## Completed:
- Server
    - Tracking TCGP recent purchase data. 
        - Modify card_info.info table columns for TCGP and SF.
    - Config files are called as needed