# Primary script
import arrow
import scripts.query_price as query_price
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
        raise SystemExit("Error: Failed to confirm db exists! Please run set_up.py")
    else:
        if not config['CONNECT'].getboolean('db_exists') == True:
            raise SystemExit("Error: Database does not exist according to config.ini. ")
        else:
            log.info(f"Fetching card data on {arrow.utcnow().format('YYYY-MM-DD')}")
            query_price.query_price()
