import os
import psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL not set")

    conn = psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row,
        autocommit=False
    )
    return conn
