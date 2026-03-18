import polars as pl
import duckdb
from dotenv import load_dotenv
import os

from config import TABLES
load_dotenv()


MOTHERDUCK_TOKEN = os.getenv("MOTHERDUCK_TOKEN")

class Repository:
    def __init__(self, db_name="my_db"):
        self.conn = duckdb.connect(f"md:{db_name}?motherduck_token={MOTHERDUCK_TOKEN}")


    def create_table(self, table_name: str, schema: str):
        self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {schema}
            )
        """)

    def insert(self, table_name: str, df: pl.DataFrame):
        # Use Arrow instead of Pandas (better)
        self.conn.register("temp_df", df.to_arrow())

        self.conn.execute(f"""
            INSERT INTO {table_name}
            SELECT * FROM temp_df
        """)

    def upsert(self, table_name: str, df: pl.DataFrame, key: str):
        self.conn.register("temp_df", df.to_arrow())

        self.conn.execute(f"""
            INSERT INTO {table_name}
            SELECT *
            FROM temp_df
            WHERE {key} NOT IN (
                SELECT {key} FROM {table_name}
            )
        """)

    def query(self, sql: str):
        return self.conn.execute(sql).fetch_df()