import psycopg2
import yaml

with open('credentials.yaml') as file:
    POSTGRES = yaml.load(file, Loader=yaml.FullLoader)['POSTGRES']


def connect_and_query(query: str, params):
    conn = psycopg2.connect(
        host=POSTGRES['HOST'],
        port=POSTGRES['PORT'],
        database=POSTGRES['DATABASE'],
        user=POSTGRES['USER'],
        password=POSTGRES['PASSWORD']
    )

    cur = conn.cursor()

    cur.execute(query, params)
    res = cur.fetchall()

    cur.close()

    return res
