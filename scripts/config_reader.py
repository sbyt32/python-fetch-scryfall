import configparser
import os
import logging
import logging_details
logging_details.log_setup()
log = logging.getLogger()

def config_reader():

    config = configparser.ConfigParser()
    config.read('config.ini')

    if os.path.exists('config.ini'):
        try: 
            config['CONNECT']
        except KeyError:
            log.critical("Missing connect info! Please run config_setup.py")
            raise SystemExit()
        else:
            return config
    else:
        log.critical("Config file does not exist! Please run config_setup.py")
        raise SystemExit()
