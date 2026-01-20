from app.db import get_db

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # -----------------------------
    # INFLUENCERS (MAIN TABLE)
    # -----------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS influencers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            platform TEXT NOT NULL,
            niche TEXT NOT NULL,
            followers INTEGER NOT NULL,
            engagement_rate REAL NOT NULL,
            price INTEGER NOT NULL,
            audit_score TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # -----------------------------
    # SAVED INFLUENCERS
    # -----------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS saved_influencers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            influencer_id INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
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
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
