import configparser
import os
import logging
log = logging.getLogger()
def config_reader():

    config = configparser.ConfigParser()
    config.read('config.ini')

    if os.path.exists('config.ini'):
        try: 
            config['CONNECT']
        except KeyError:
            log.critical("Connect info does not exist! Please run config_setup.py")
            raise SystemExit()
        else:
            return config
    else:
        log.critical("Error: Config file does not exist! Please run config_setup.py")
        raise SystemExit()    
