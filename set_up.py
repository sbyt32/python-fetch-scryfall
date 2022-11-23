import configparser
import os
import logging
import logging_details
from scripts.setup_scripts import cfg_setup, _set_up_db

logging_details.log_setup()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

cfg_reconfig = ''
db_reconfig = ''
# * Have to double check that we have a config.ini. Otherwise, can't do much, really
if os.path.exists('config_files/config.ini'):
    cfg_reconfig = input("config files already exist, replace? y/n ").lower() or "No"

if not os.path.exists('config_files/config.ini') or cfg_reconfig in ["y", "yes"]:
    
    if cfg_reconfig in ["y", "yes"]:
        cfg_log_msg = "Overwriting config.ini"
    else:
        cfg_log_msg = "File config_files/config.ini does not exist, creating..."

    log.info(cfg_log_msg)
    cfg_setup()

# * Now that the config is 100% certainly made, we can crack it open.
cfg = configparser.ConfigParser()
cfg.read('config_files/config.ini')

# * Create DB strucutre, if does not exist.
if cfg['CONNECT'].getboolean('db_exists') == True:
    db_reconfig = input(f"Database {cfg['CONNECT']['dbname']} is already set up, would you like to set it up again? ")

if cfg['CONNECT'].getboolean('db_exists') == False or db_reconfig in ["y", "yes"]:

    if db_reconfig in ["y", "yes"]:
        db_log_msg = "Recreating Database structure!"
    else:
        db_log_msg = "Database does not exist, creating..."

    log.info(db_log_msg)

    if _set_up_db() == True:
        with open('config.ini', 'w') as config_update:
            cfg['CONNECT']['db_exists'] = "true"
            cfg.write(config_update)