from fastapi import APIRouter, HTTPException
from app.db import get_db
from datetime import datetime

router = APIRouter(prefix="/influencers", tags=["Influencers"])

@router.post("/register")
def register_influencer(payload: dict):
    required = [
        "name",
        "platform",
        "niche",
        "followers",
        "avg_views",
        "price_per_post",
    ]

    for field in required:
        if field not in payload:
            raise HTTPException(status_code=400, detail=f"Missing {field}")

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO influencers
        (name, platform, niche, followers, avg_views, price_per_post, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        payload["name"],
        payload["platform"],
        payload["niche"],
        payload["followers"],
        payload["avg_views"],
        payload["price_per_post"],
        datetime.utcnow().isoformat()
    ))

    db.commit()

    return {"status": "ok"}
