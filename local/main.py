import os
import configparser
from pick import pick
from add_card import add_card
from scripts.postgres_scripts.db_setup import _set_up
import scripts

if __name__ == "__main__":
    config = scripts.config_reader()
    try:
        config['CONNECT']['db_exists']
    except KeyError:
        print('Setting up!') # Change these to logging, eventually.
        _set_up()
        config['CONNECT']['db_exists'] = "True"
        with open('config.ini', 'w') as config_update:
            config.write(config_update)
        add_card()
    else:
        add_card()

