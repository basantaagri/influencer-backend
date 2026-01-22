from fastapi import APIRouter
from app.db import get_supabase

router = APIRouter()

# -------------------------------------------------
# POST /seed
# DEV-ONLY: Seed influencers (IDEMPOTENT)
# Uses UPSERT on username to avoid duplicates
# -------------------------------------------------
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
            "audit_score": 82,  # ✅ NUMERIC (SAFE)
            "profile_url": "https://instagram.com/tech_guru",
        },
        {
            "username": "fashion_diva",
            "platform": "Instagram",
            "niche": "Fashion",
            "followers": 98000,
            "engagement_rate": 3.8,
            "price": 4500,
            "audit_score": 76,  # ✅ NUMERIC (SAFE)
            "profile_url": "https://instagram.com/fashion_diva",
        },
    ]

    # ✅ CRITICAL FIX — DO NOT CHANGE
    # Idempotent upsert prevents duplicate rows forever
    res = (
        supabase
        .table("influencers")
        .upsert(
            data,
            on_conflict="username"
        )
        .execute()
    )

    if res.error:
        return {
            "status": "error",
            "message": res.error.message,
        }

    return {
        "status": "seeded",
        "count": len(data),
    }
