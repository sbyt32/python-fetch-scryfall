import os

# ? Where do you want this to go?

def create_directory():
    paths_to_check = [
        'data/cards_to_query.ndjson',
        'tracking/'
    ]
    for paths in paths_to_check: 
        if not os.path.exists(paths):
            os.makedirs(paths)