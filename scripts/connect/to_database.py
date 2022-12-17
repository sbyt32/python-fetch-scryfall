import psycopg
import logging
from scripts.config_reader import config_reader
log = logging.getLogger()

def connect_db(**kwargs):
    """Always have two variables into this, connection and cursor. Default to `conn, cur = connect_db`
    \nOptional (to return as dict): 
        \n`from psycopg.rows import dict_row`
        \n`connect_db(row_factory = dict_row)` 
    
    \n[More info about psycopg](https://www.psycopg.org/psycopg3/docs/api/connections.html#psycopg.Connection)
    """
    db_info = config_reader("CONNECT", 'database')
    log.debug(f"Connecting to database: {db_info['dbname']}")
    conn_info = psycopg.conninfo.make_conninfo(**db_info)
    
    conn = psycopg.connect(conn_info, **kwargs)
    cur  = conn.cursor()

    return conn, cur