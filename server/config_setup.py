import configparser
import os


config = configparser.ConfigParser()
config.read('config.ini')

if os.path.exists('config.ini'):
    config_create = input("config.ini already exists, replace? y/n ")
    if not config_create == "y" and not config_create == "n":
        print("Invalid Input, type y or n")

if not os.path.exists('config.ini') or config_create == "y":
    config['DEFAULT']               = {}
    config['CONNECT']               = {}
    config['DEFAULT']['path']       = ""
    config['DEFAULT']['config']     = "config.ini"
    config['CONNECT']["host"]       = input("Host Address: (Default: localhost) ") or "localhost"
    config['CONNECT']["user"]       = input("Username: ")
    config['CONNECT']["pass"]       = input(f"Password for {config['CONNECT']['user']}: ")
    config['CONNECT']["dbname"]     = input("Database: (Default: price_tracker) ") or "price_tracker"
    config["CONNECT"]['db_exists']  = input("Does Database Exist? y/n (Default: y) ") or "y"

    # Database existance, if you ran the script in the /local/ folder, yes
    if config["CONNECT"]['db_exists'] in ["yes", "y"]:
        config["CONNECT"]['db_exists']  = "true"
    elif config["CONNECT"]['db_exists'] in ["No", "n"]:
        config["CONNECT"]['db_exists']  = "false"
    else:
        print("Invalid value, assuming database does not exist.")
        config["CONNECT"]['db_exists']  = "false"

    with open('config.ini', 'w') as config_update:
        config.write(config_update)