import psycopg2
import psycopg2.errors
from scripts.config_read import config_reader


def append_query(query:dict):
    config = config_reader()
    HOST = config['CONNECT']['host']
    USER = config['CONNECT']['user']
    PASS = config['CONNECT']['pass']
    DBNAME = config['CONNECT']['dbname']


    if query is not None:
        connect = psycopg2.connect(dbname = DBNAME, user=USER, password=PASS, host=HOST)

        cur = connect.cursor()
        # * Check if it exists already. If == 0, then write it.
        cur.execute("SELECT * from card_info.info where id = %s AND set= %s", (query['id'], query['set']))
        if len(cur.fetchall()) == 0:
        
            add_info_to_postgres = """
                INSERT INTO card_info.info (name, set, id, uri)

                VALUES (%s,%s,%s,%s) 
                ON CONFLICT DO NOTHING 
                """

                
            cur.execute(add_info_to_postgres, (query['name'], query['set'], query['id'], query['uri']))
            
            connect.commit()
        else:
            print(f"{query['name']} from {query['set']} is already being tracked!")

        # Here is where repeat search would be
        # ? Should I put that as a separate script?