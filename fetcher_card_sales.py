# This script grabs the price of recent sale data.
import arrow
from scripts.fetch_sale_data import fetch_tcg_prices
import scripts.config_reader as config_reader
import logging
import logging_details
logging_details.log_setup()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

if __name__ == "__main__":
    cfg = config_reader.config_reader()
    try:
        cfg['CONNECT']['db_exists']
    except KeyError:
        log.error("Cannot confirm that the database exist. Does config.ini exist?")
        raise SystemExit
    else:
        if not cfg['CONNECT'].getboolean('db_exists') == True:
            log.error("Database does not exist according to config.ini.")
            raise SystemExit
        else:
            log.info(f"Fetching sale data on {arrow.utcnow().format('YYYY-MM-DD')}")
            fetch_tcg_prices()
