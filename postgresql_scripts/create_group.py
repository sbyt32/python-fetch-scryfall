import psycopg2
from variables import HOST, USER, PASS, DBNAME

def _create_card_group(id:str, set:str, group:list):
    conn = psycopg2.connect(dbname = DBNAME, user=USER, password=PASS, host=HOST)
    cur = conn.cursor()

    cur.execute(
        f""" INSERT INTO card_info.groups

        VALUES (
            '{id}',
            '{set}',
            '{group}'
        )
        
        """
    )
    conn.commit()
    conn.close()

    # * Example
    # cur.execute(
    #     """ INSERT INTO card_info.groups

    #     VALUES (
    #         '69',
    #         'ktk',
    #         '{"fetchland", "uw_phoenix"}'
    #     )
        
    #     """
    # )
