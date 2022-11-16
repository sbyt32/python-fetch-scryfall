import psycopg2
import logging
import scripts.config_reader as config_reader
log = logging.getLogger()


def connect():
    config = config_reader.config_reader()
    conn = psycopg2.connect(
        host        =   config['CONNECT']['host'],
        user        =   config['CONNECT']['user'],
        password    =   config['CONNECT']['pass'],
        dbname      =   config['CONNECT']['dbname']
    )
    cur = conn.cursor()

    return conn, cur