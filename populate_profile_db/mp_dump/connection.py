import psycopg2
import yaml
from dotenv import dotenv_values

env_variables = dotenv_values(".env")


def connect_and_query(query: str, params):
    conn = psycopg2.connect(
        host=env_variables['POSTGRES_HOST'],
        port=env_variables['POSTGRES_PORT'],
        database=env_variables['POSTGRES_DATABASE'],
        user=env_variables['POSTGRES_USER'],
        password=env_variables['POSTGRES_PASSWORD']
    )

    cur = conn.cursor()

    cur.execute(query, params)
    res = cur.fetchall()

    cur.close()

    return res
