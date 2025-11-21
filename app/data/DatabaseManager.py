import logging

import pandas as pd
import psycopg
from psycopg import sql

from app.config import config


logger = logging.getLogger(__name__)


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

    def fetch(self, query, params=None, parse_dates=None):
        return pd.read_sql_query(
            query, self.conn, params=params, parse_dates=parse_dates
        )

    def fetch_table(self, table, parse_dates=None):
        query = sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(table))
        return self.fetch(
            query.as_string(self.conn), params=None, parse_dates=parse_dates
        )

    def upsert_df(self, df, table, conflict_columns, update_columns):
        if df.empty:
            return

        with self.conn.cursor() as cur:
            for _, row in df.iterrows():
                columns = list(df.columns)
                values = [row[col] for col in columns]
                insert_stmt = sql.SQL(
                    "INSERT INTO {table} ({fields}) VALUES ({placeholders})"
                ).format(
                    table=sql.Identifier(table),
                    fields=sql.SQL(", ").join(map(sql.Identifier, columns)),
                    placeholders=sql.SQL(", ").join(sql.Placeholder() * len(columns)),
                )
                set_clause = sql.SQL(", ").join(
                    sql.SQL("{} = EXCLUDED.{}").format(
                        sql.Identifier(col), sql.Identifier(col)
                    )
                    for col in update_columns
                )
                conflict_stmt = sql.SQL(
                    " ON CONFLICT ({conflict}) DO UPDATE SET {set_clause}"
                ).format(
                    conflict=sql.SQL(", ").join(map(sql.Identifier, conflict_columns)),
                    set_clause=set_clause,
                )
                query = insert_stmt + conflict_stmt
                cur.execute(query, values)
            self.conn.commit()
