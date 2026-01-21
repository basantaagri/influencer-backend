from fastapi import APIRouter
from app.db import get_db

router = APIRouter()

@router.post("/seed")
def seed_influencers():
    conn = get_db()
    cur = conn.cursor()

    demo = [
        ("tech_guru", "Instagram", "Tech", 120000, 4.2, 5000, "A"),
        ("fashion_diva", "Instagram", "Fashion", 98000, 3.8, 4500, "B"),
        ("finance_bro", "Twitter", "Finance", 65000, 5.1, 6000, "A"),
    ]

    for d in demo:
        cur.execute(
            """
            INSERT INTO influencers
            (username, platform, niche, followers, engagement_rate, price, audit_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            d
        )

    conn.commit()
    conn.close()

    return {"status": "seeded"}
