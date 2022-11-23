# Primary script
import arrow
from scripts.query_price import query_price
import scripts.config_reader as config_reader
import logging
import logging_details
logging_details.log_setup()
log = logging.getLogger()
log.setLevel(logging.INFO)

if __name__ == "__main__":
    cfg = config_reader.config_reader('FILE_DATA', 'config')
    try:
        cfg['db_exists']
    except KeyError:
        log.error("Cannot confirm that the database exist. Does config_files/config.ini exist?")
        raise SystemExit
    else:

        if not bool(cfg['db_exists']) == True:
            log.error("Database does not exist according to config_files/config.ini.")
            raise SystemExit()
        else:
            log.info(f"Fetching card data on {arrow.utcnow().format('YYYY-MM-DD')}")
            query_price()

