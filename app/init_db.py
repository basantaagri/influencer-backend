from app.db import get_db
from datetime import datetime

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # -----------------------------
    # TABLES
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

    cur.execute("""
        CREATE TABLE IF NOT EXISTS saved_influencers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            influencer_id INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

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

    # -----------------------------
    # SEED DEMO DATA (CRITICAL)
    # -----------------------------
    cur.execute("SELECT COUNT(*) FROM influencers")
    count = cur.fetchone()[0]

    if count == 0:
        demo_data = [
            ("techguru", "Instagram", "Tech", 120000, 4.2, 5000, "A"),
            ("fashiondiary", "Instagram", "Fashion", 98000, 3.8, 4000, "B"),
            ("fitlife", "YouTube", "Fitness", 210000, 5.1, 7000, "A"),
        ]

        cur.executemany("""
            INSERT INTO influencers
            (username, platform, niche, followers, engagement_rate, price, audit_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, demo_data)

    conn.commit()
    conn.close()
