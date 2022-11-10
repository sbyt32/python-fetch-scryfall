# Primary script
import scripts
import os
import scripts.config_reader as config_reader
from scripts.update_old_data import update_old_data


if __name__ == "__main__":
    # ? Come up with a better way to check if the old data is still existing?
    config = config_reader.config_reader()
    try:
        config['CONNECT']['db_exists']
    except KeyError:
        raise SystemExit("Error: Failed to confirm db exists! Please run config_setup.py")
    else:
        if not config['CONNECT'].getboolean('db_exists') == True:
            raise SystemExit("Error: Database does not exist according to config.ini. ")
        
        if not os.path.exists('data/tracking_old') and os.path.exists('data/tracking'):
            update_old_data()
        else:
            scripts.query_price()