# Primary script
import arrow
# from fetcher.query_price import query_price
from scripts.query_price import query_price
import scripts.config_reader as config_reader
import logging
import logging_details
logging_details.log_setup()
log = logging.getLogger()
log.setLevel(logging.INFO)

if __name__ == "__main__":
    # ? Come up with a better way to check if the old data is still existing?
    config = config_reader.config_reader()
    try:
        config['CONNECT']['db_exists']
    except KeyError:
        log.error("Cannot confirm that the database exist. Does config.ini exist?")
        raise SystemExit
    else:
        if not config['CONNECT'].getboolean('db_exists') == True:
            log.error("Database does not exist according to config.ini.")
            raise SystemExit()
        else:
            log.info(f"Fetching card data on {arrow.utcnow().format('YYYY-MM-DD')}")
            query_price()
