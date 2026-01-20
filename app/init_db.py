from app.db import get_db

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # -----------------------------
    # SAVED INFLUENCERS
    # -----------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS saved_influencers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            influencer_id INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # -----------------------------
    # ORDERS
    # -----------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            influencer_id INTEGER NOT NULL,
            influencer_name TEXT NOT NULL,
            price INTEGER NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
