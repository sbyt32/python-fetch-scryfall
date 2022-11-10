# Primary script
import scripts
import os
# from scripts.add_card_scripts.postgres_scripts.db_setup import _set_up
from scripts.update_old_data import update_old_data
if __name__ == "__main__":
    # ? Come up with a better way to check if the old data is still existing?
    if not os.path.exists('data/tracking_old') and os.path.exists('data/tracking'):
        update_old_data()
    else:
        scripts.query_price()