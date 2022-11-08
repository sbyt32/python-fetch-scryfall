# Primary script
import scripts
import os
from postgresql_scripts.db_setup import _set_up
from update_old_data import update_old_data
if __name__ == "__main__":
    # ? Come up with a better way to check if the old data is still existing?
    if not os.path.exists('data/tracking_old'):
        _set_up()
        update_old_data()
    else:
        scripts.query_price()