import configparser
import os
import logging
import logging_details
logging_details.log_setup()
log = logging.getLogger()

def config_reader(section, cfg:str):
    """Checking to see if the config works.
    \n hello
    """


    parser = configparser.ConfigParser()
    cfg_file = f'config_files/{cfg}.ini'
    parser.read(cfg_file)
    db = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Hi")
    return db
    # config.read(cfg_file)

    # if os.path.exists(cfg_file):
    #     try: 
    #         config['CONNECT']
    #     except KeyError:
    #         log.critical("Missing connect info! Please run config_setup.py")
    #         raise SystemExit()
    #     else:
    #         return config
    # else:
    #     log.critical("Config file does not exist! Please run config_setup.py")
    #     raise SystemExit()
