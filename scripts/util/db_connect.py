import psycopg2

from variables import HOST, USER, PASS, DBNAME
# ? variables.py contains the following: 
# * HOST    = Server Name
# * USER    = Username
# * PASS    = Password
# * DBNAME  = Database name

def _connect_to_db():
    connect = psycopg2.connect(dbname = DBNAME, user=USER, password=PASS, host=HOST)

    cur = connect.cursor()

    return connect, cur

# TODO: work this out
# class connect_to_db:
#     def __init__(self) -> None:
#         self.connect = psycopg2.connect(dbname = DBNAME, user=USER, password=PASS, host=HOST)
#         self.cur = self.connect.cursor()
    
#     def _collapse_db(self):
#         self.connect.close()