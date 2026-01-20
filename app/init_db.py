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

    # -----------------------------
    # ONE-TIME SAFE SEED (ONLY IF EMPTY)
    # -----------------------------
    cur.execute("SELECT COUNT(*) FROM influencers")
    count = cur.fetchone()[0]

    if count == 0:
        cur.execute("""
            INSERT INTO influencers
            (username, platform, niche, followers, engagement_rate, price, audit_score)
            VALUES
            ('FitLifeRiya', 'Instagram', 'Fitness', 120000, 3.9, 200, 'Medium'),
            ('TechWithAman', 'YouTube', 'Technology', 98000, 4.5, 350, 'Low'),
            ('DailyFinance', 'YouTube', 'Finance', 64000, 2.8, 300, 'High'),
            ('StyleByNeha', 'Instagram', 'Fashion', 150000, 4.2, 400, 'Low'),
            ('FoodieRaj', 'Instagram', 'Food', 82000, 3.6, 180, 'Medium')
        """)

    conn.commit()
    conn.close()
