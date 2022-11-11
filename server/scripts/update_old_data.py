import csv
import re
import os
import ndjson
import psycopg2
import scripts.config_reader

# Localhost functions perfectly fine on the server.

def use_regex(input_text):
    # ? What is this for again?
    text = re.sub("\s(([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?(:([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?)+)", "", input_text)
    return text

def null_check(value):
    if value == '':
        return None
    return value

def update_old_data():
    config = scripts.config_reader.config_reader()
    HOST = config['CONNECT']['host']
    USER = config['CONNECT']['user']
    PASS = config['CONNECT']['pass']
    DBNAME = config['CONNECT']['dbname']
    conn = psycopg2.connect(dbname = DBNAME, user=USER, password=PASS, host=HOST)

    cur = conn.cursor()

# Due to changing from .csv to a postgresql database, need to transform the filename a lil.
    if not os.path.exists('data/tracking_old'):
        os.rename('data/tracking/', 'data/tracking_old')
        os.makedirs('data/tracking')
        for dirpath, dirs, files in os.walk('data/tracking_old/'):
                
            for filename in files:
                old_file = os.path.join(dirpath, filename)
                set_name = re.findall('[A-Za-z0-9]+', dirpath)[-1]

                with open(old_file, newline='') as to_transform:
                    read = csv.reader(to_transform, quoting=csv.QUOTE_MINIMAL)

                    with open(f'data/tracking/{set_name}_{filename}', 'w' , newline='') as fixed_list:
                        writer = csv.writer(fixed_list, quoting=csv.QUOTE_MINIMAL)
                        for x in read:
                            if len(x) == 6:
                                x[0] = use_regex(x[0])
                                writer.writerow(x)

    # Insert all the existing info into the card_data table
    for dirpath, dirs, files in os.walk('data/tracking'): 
        for filename in files:
            set_id = re.findall('[A-Za-z0-9]+', filename)

            with open(f'data/tracking/{filename}',newline='') as data_to_dump:
                reader = csv.reader(data_to_dump, quoting=csv.QUOTE_MINIMAL)
                next(reader)
                for cards in reader:
                    cur.execute(
                    """
                    INSERT INTO card_data (set, id, date, usd, usd_foil, euro, euro_foil, tix) 
                    
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

                    ON CONFLICT DO NOTHING
                    """, 
                    (   
                        set_id[0],
                        set_id[1],
                        null_check(cards[1]),
                        null_check(cards[2]),
                        null_check(cards[3]),
                        null_check(cards[4]),
                        null_check(cards[5])
                        )
                    )

    # Place all the information regarding card data into the file.
    with open('data/cards_to_query.ndjson') as cards_to_query:
        reader = ndjson.reader(cards_to_query)
        for cards in reader:

            # * See if the table exists, already
            if bool(cur.execute(f"SELECT * from card_info.info where id='{cards['id']}' AND set='{cards['set']}'")) == False:

                cur.execute("""
                INSERT INTO card_info.info (name, set, id, uri)

                VALUES (%s,%s,%s,%s) 
                ON CONFLICT DO NOTHING 
                """, (cards['name'],cards['set'],cards['id'],cards['uri']))

    conn.commit()