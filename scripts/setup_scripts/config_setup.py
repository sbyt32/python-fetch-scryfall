import configparser
import os
import re

def cfg_setup():
    # cfg_files = [("config.ini", "cfg"), ("database.ini", ""), ("tokens.ini", "")]

    cfg_folder_path = input("Config folder (Default: config_files): ") or "config_files"
    if not re.match(r"^.*/$", cfg_folder_path, re.IGNORECASE):
        cfg_folder_path += '/'
    if not os.path.exists(cfg_folder_path):
        os.makedirs(cfg_folder_path)

    # * A config file just to get some basic info and where other data is.
    cfg = configparser.ConfigParser()
    cfg.read(cfg_folder_path + 'config.ini')

    cfg['FILE_DATA']                  = {}
    cfg['FILE_DATA']['config_path']   = cfg_folder_path + "config.ini"
    cfg['FILE_DATA']['token_path']    = cfg_folder_path + "token.ini"
    cfg['FILE_DATA']['database_path'] = cfg_folder_path + "database.ini"
    cfg['FILE_DATA']['db_exists']     = input("Does Database Exist? y/n (Default: y) ") or "y"

    # Database existance, if you ran the script in the /local/ folder, yes
    if cfg['FILE_DATA']['db_exists'] in ["yes", "y"]:
        cfg['FILE_DATA']['db_exists']  = "true"
    elif cfg['FILE_DATA']['db_exists'] in ["No", "n"]:
        cfg['FILE_DATA']['db_exists']  = "false"
    else:
        print("Invalid value, assuming database does not exist.")
        cfg['FILE_DATA']['db_exists']  = "false"

    # * A config file to hold connection information, mostly to pass into psycopg3 
    database = configparser.ConfigParser()
    database.read(cfg_folder_path + 'database.ini')

    database['CONNECT']                  = {}
    database['UPDATES']                  = {}
    database['CONNECT']["host"]          = input("Host Address: (Default: localhost) ") or "localhost"
    database['CONNECT']["user"]          = input("Username: ")
    database['CONNECT']["pass"]          = input(f"Password for {database['CONNECT']['user']}: ")
    database['CONNECT']["dbname"]        = input("Database: (Default: price_tracker) ") or "price_tracker"

    # * A config file for tokens! Tokens for general access, writing, and price data.
    tokens = configparser.ConfigParser()
    tokens.read(cfg_folder_path + 'tokens.ini')

    tokens[database['CONNECT']["host"]]                  = {}
    tokens[database['CONNECT']["host"]]['sec_token']     = input("Security Token (For access): ") or "testing"
    tokens[database['CONNECT']["host"]]['write_token']   = input("Writing Token (For writing to the DB!): ") or "testing"
    tokens[database['CONNECT']["host"]]['price_token']   = input("Price Token (For accessing price information): ") or "testing"


    with open(cfg_folder_path + 'config.ini', 'w') as config_update:
        cfg.write(config_update)

    with open(cfg_folder_path + 'database.ini', 'w') as database_update:
        database.write(database_update)

    with open(cfg_folder_path + 'tokens.ini', 'w') as tokens_update:
        tokens.write(tokens_update)

cfg_setup()