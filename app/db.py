import os
import psycopg2
from psycopg2.extras import RealDictCursor

# -------------------------------------------------
# DATABASE CONNECTION (SUPABASE POSTGRES)
# -------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

def get_db():
    conn = psycopg2.connect(
        DATABASE_URL,
        cursor_factory=RealDictCursor
    )
    return conn
