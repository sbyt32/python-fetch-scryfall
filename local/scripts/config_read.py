import configparser
import os
def config_reader():
    config = configparser.ConfigParser()
    config.read('config.ini')
    if os.path.exists('config.ini'):
        try: 
            config['CONNECT']
        except KeyError:
            raise SystemExit("Error: Connect info does not exist! Please run config_setup.py")
        else:
            return config
    else:
        raise SystemExit("Error: Config file does not exist! Please run 'config_setup.py'")    
