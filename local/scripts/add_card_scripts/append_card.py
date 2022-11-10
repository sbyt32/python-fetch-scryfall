import psycopg2
import psycopg2.errors
import os
import ndjson
from variables import HOST, USER, PASS, DBNAME


def append_query(query:dict):
    # ? May be worth having a local version of the database?
    card_path = 'data/cards_to_query.ndjson'
    if not os.path.exists(card_path):
        os.makedirs('data')
        open(card_path, 'x')


    with open(card_path) as card_database:
        cards_to_compare = ndjson.reader(card_database)          

        duplicate = False

        for card in cards_to_compare:
            if card == query:
                duplicate = True
                break

        if duplicate:
            return # TODO: This needs to see if the content is already there
        else:
            if query is not None:
                connect = psycopg2.connect(dbname = DBNAME, user=USER, password=PASS, host=HOST)

                cur = connect.cursor()
                # * Check if it exists already. If == 0, then write it.
                if bool(cur.execute(f"SELECT * from card_info.info where id='{query['id']}' AND set='{query['set']}'")) == 0:
                    
                    add_info_to_postgres = """
                    INSERT INTO card_info.info (name, set, id, uri)

                    VALUES (%s,%s,%s,%s) 
                    ON CONFLICT DO NOTHING 
                    """

                    
                    cur.execute(add_info_to_postgres, (query['name'], query['set'], query['id'], query['uri']))
                    
                    connect.commit()

                    # Locally write it, as well. 
                    with open(card_path, 'a') as cards_to_write:
                        writer = ndjson.writer(cards_to_write)
                        writer.writerow(query)
                        # Here is where repeat search would be
                        # ? Should I put that as a separate script?