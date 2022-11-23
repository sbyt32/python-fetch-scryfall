import psycopg2
import logging
from scripts.config_reader import config_reader
log = logging.getLogger()


def connect():
    db_info = config_reader("CONNECT","database")
    conn = psycopg2.connect(
        **db_info
    )
    cur = conn.cursor()

    return conn, cur