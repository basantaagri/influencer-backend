from fastapi import APIRouter, HTTPException
from app.db import get_supabase

router = APIRouter()

@router.post("/seed")
def seed_influencers():
    supabase = get_supabase()

    data = [
        {
            "username": "tech_guru",
            "platform": "Instagram",
            "niche": "Tech",
            "followers": 120000,
            "engagement_rate": 4.2,
            "price": 5000,
            "audit_score": "A",
        },
        {
            "username": "fashion_diva",
            "platform": "Instagram",
            "niche": "Fashion",
            "followers": 98000,
            "engagement_rate": 3.8,
            "price": 4500,
            "audit_score": "B",
        },
    ]

    res = supabase.table("influencers").insert(data).execute()

    # ✅ NEW supabase-py behavior
    if not res.data:
        raise HTTPException(
            status_code=500,
            detail="Insert failed (no data returned from Supabase)",
        )

    return {
        "status": "seeded",
        "count": len(res.data),
    }
