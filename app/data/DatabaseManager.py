import pandas as pd
import psycopg
from psycopg import sql

from app.config import config


class PostgresDB:
    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = psycopg.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
        )
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.conn and not self.conn.closed:
            self.conn.close()

    def execute(self, query, params=None):
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            self.conn.commit()

    def fetch_raw(self, query, params=None, fetch_one=False):
        with self.conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(query, params)
            if fetch_one:
                return cur.fetchone()
            return cur.fetchall()

    def fetch(self, query, params=None):
        return pd.read_sql_query(query, self.conn, params=params)

    def fetch_table(self, table):
        query = sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(table))
        return self.fetch(query.as_string(self.conn), params=None)
