# MTG Price Fetcher
> A simple price fetcher for Magic: The Gathering, powered via Scryfall's API and written in Python.

## How it works

### set_up.py
Asks for certain information for database usage. That data is stored in `config_files/*.ini`. It will also create a database for you and set everything up for the scripts to work correctly.  **Run this before anything else** or else everything else will fail to run. 

**Note**: Failing to input token values returns back *testing* as your token. 

### api.py
`api.py` is the API for the project, run it with [hypercorn](https://pgjones.gitlab.io/hypercorn/). It is currently the only way to add cards to be tracked at the moment.

    hypercorn api:app

Uvicorn might work, but have not built with it in mind.

Docs are a WIP. Use localhost:8000/docs for help.

### fetcher_card_price.py
`fetcher_card_price.py` pulls prices from Scryfall, which is powered by TCGPlayer. Once ran, it will parse through the cards that are in the database created in `set_up.py` and send requests to get prices for each of the cards. Those prices are stored in the aformentioned database. All formatting for collector number and set names is pulled from [Scryfall](https://scryfall.com/sets).

Run this script once a day, using `crontab` or any sort of scheduling program.

### fetcher_card_sales.py
`fetcher_card_sales.py` pulls sales from TCGPlayer, using the same cards that are being tracked. Those prices are placed into the database and can be called via the API or with SQL queries. 

Run this script once a week to every other week, there is not much need to fetch daily.

### logging_details.py
Logging setup, the data will be placed in the folder `logs/`. Not much to it.

Example `*.log` output
```log
2022-11-23 15:46:13,979 | INFO     | add_remove_db_data.py | Now tracking: Thalia, Guardian of Thraben from Innistrad: Crimson Vow
```

## Libraries
    arrow
    requests
    psycopg[binary]
    fastapi
    hypercorn

## TODO:
- Server
    - Add card groups
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