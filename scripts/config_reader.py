import configparser
import os
import logging
import logging_details
logging_details.log_setup()
log = logging.getLogger()

def config_reader(section:str, cfg:str):
    """A way to read and parse the different config files.
    \nExample = `config_reader('CONNECT', 'cfg')
| input   | desc                       |
|---------|----------------------------|
| section | header to get in .ini file |
| cfg     | .ini file name             | 
-------
    \n- config.ini
    \n  - FILE_DATA
    \n          - config_path `str`
    \n          - token_path `str`
    \n          - database_path `str`
    \n          - db_exists `bool`
    \n- database.ini
    \n  - CONNECT
    \n          - host `str`
    \n          - user `str`
    \n          - password `str`
    \n          - dbname `str`
    \n  - UPDATES
    \n          - tcg_sales `str`
    \n- tokens.ini
    \n  - CONNECT
    \n          - sec_token `str`
    \n          - write_token `str`
    \n          - price_token `str`
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
        raise Exception(f'Section {section} not found in the {cfg_file} file')
    return db
