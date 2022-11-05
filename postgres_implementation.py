import psycopg2
import psycopg2.errors
import csv
import os
import re
import ndjson
# from postgresql_scripts.create_table import create_table

# ? variables.py contains the following: 
# * HOST    = Server Name
# * USER    = Username
# * PASS    = Password
# * DBNAME  = Database name
from variables import HOST, USER, PASS, DBNAME

conn = psycopg2.connect(dbname = DBNAME, user=USER, password=PASS, host=HOST)

cur = conn.cursor()

# Todo: Create cards_info.info script
# Todo: https://www.folkstalk.com/2022/09/insert-if-not-exists-postgresql-with-code-examples.html

# * Execute a query

# * Check if info to pull exists.
# ? Maybe consider pulling the data from the database instead.
# with open('data/cards_to_query.ndjson') as cards_to_query:
#     reader = ndjson.reader(cards_to_query)
#     for cards in reader:
#         if bool(cur.execute(f"SELECT * from card_info.info where id='{cards['id']}' AND set='{cards['set']}'")) == 0:
#             # * See if the table 
#             cur.execute(f"INSERT INTO card_info.info (name, set, id, uri) VALUES ('{cards['name']}', '{cards['set']}', '{cards['id']}', '{cards['uri']}') ON CONFLICT DO NOTHING")
#             conn.commit()


        
conn.commit()