import configparser
import os

def cfg_setup():
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')

    cfg['DEFAULT']                  = {}
    cfg['CONNECT']                  = {}
    cfg['DEFAULT']['path']          = ""
    cfg['DEFAULT']['config']        = "config.ini"
    cfg['CONNECT']["host"]          = input("Host Address: (Default: localhost) ") or "localhost"
    cfg['CONNECT']["user"]          = input("Username: ")
    cfg['CONNECT']["pass"]          = input(f"Password for {cfg['CONNECT']['user']}: ")
    cfg['CONNECT']["dbname"]        = input("Database: (Default: price_tracker) ") or "price_tracker"

    # Tokens for general access, writing, and price data.
    cfg['CONNECT']['sec_token']     = input("Security Token (For access): ") or "testing"
    cfg['CONNECT']['write_token']   = input("Writing Token (For writing to the DB!): ") or "testing"
    cfg['CONNECT']['price_token']   = input("Price Token (For accessing price information): ") or "testing"

    cfg["CONNECT"]['db_exists']     = input("Does Database Exist? y/n (Default: y) ") or "y"


    # Database existance, if you ran the script in the /local/ folder, yes
    if cfg["CONNECT"]['db_exists'] in ["yes", "y"]:
        cfg["CONNECT"]['db_exists']  = "true"
    elif cfg["CONNECT"]['db_exists'] in ["No", "n"]:
        cfg["CONNECT"]['db_exists']  = "false"
    else:
        print("Invalid value, assuming database does not exist.")
        cfg["CONNECT"]['db_exists']  = "false"


    with open('config.ini', 'w') as config_update:
        cfg.write(config_update)