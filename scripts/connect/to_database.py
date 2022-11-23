import psycopg2
import logging
from scripts.config_reader import config_reader
log = logging.getLogger()


def connect():
    config = config_reader("CONNECT","database")
    conn = psycopg2.connect(
        host        =   config['CONNECT']['host'],
        user        =   config['CONNECT']['user'],
        password    =   config['CONNECT']['pass'],
        dbname      =   config['CONNECT']['dbname']
    )
    cur = conn.cursor()

    return conn, cur