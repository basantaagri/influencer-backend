from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.db import get_supabase

# -------------------------------------------------
# ROUTER
# NOTE:
# This router is mounted at:
#   /influencers
# in main.py
# -------------------------------------------------
router = APIRouter(
    prefix="/influencers",
    tags=["Influencers"],
)

# -------------------------------------------------
# GET /influencers
# List influencers with optional filters + pagination
# RETURNS PURE ARRAY (frontend-safe)
# -------------------------------------------------
@router.get("/")
def list_influencers(
    platform: Optional[str] = Query(None),
    niche: Optional[str] = Query(None),
    min_followers: Optional[int] = Query(None, ge=0),

    # Pagination
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
):
    supabase = get_supabase()

    offset = (page - 1) * per_page
    limit = per_page

    query = supabase.table("influencers").select("*")

    # ✅ IGNORE "All" FILTERS (CRITICAL)
    if platform and platform != "All":
        query = query.eq("platform", platform)

    if niche and niche != "All":
        query = query.eq("niche", niche)

    if min_followers is not None:
        query = query.gte("followers", min_followers)

    res = query.range(offset, offset + limit - 1).execute()

    # ✅ FRONTEND GUARANTEE — ALWAYS ARRAY
    return res.data or []


# -------------------------------------------------
# POST /influencers
# Create a new influencer
# -------------------------------------------------
@router.post("/")
def create_influencer(payload: dict):
    supabase = get_supabase()

    required_fields = [
        "username",
        "platform",
        "niche",
        "followers",
        "engagement_rate",
        "price",
        "audit_score",
    ]

    for field in required_fields:
        if field not in payload:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required field: {field}",
            )

    res = supabase.table("influencers").insert(payload).execute()

    return {
        "status": "created",
        "data": res.data[0] if res.data else None,
    }


# -------------------------------------------------
# GET /influencers/{influencer_id}
# Fetch single influencer
# -------------------------------------------------
@router.get("/{influencer_id}")
def get_influencer(influencer_id: int):
    supabase = get_supabase()

    res = (
        supabase
        .table("influencers")
        .select("*")
        .eq("id", influencer_id)
        .single()
        .execute()
    )

    if not res.data:
        raise HTTPException(status_code=404, detail="Influencer not found")

    return res.data


# -------------------------------------------------
# PATCH /influencers/{influencer_id}
# Update influencer
# -------------------------------------------------
@router.patch("/{influencer_id}")
def update_influencer(influencer_id: int, payload: dict):
    supabase = get_supabase()

    if not payload:
        raise HTTPException(status_code=400, detail="Empty update payload")

    res = (
        supabase
        .table("influencers")
        .update(payload)
        .eq("id", influencer_id)
        .execute()
    )

    return {
        "status": "updated",
        "updated_rows": len(res.data or []),
    }


# -------------------------------------------------
# DELETE /influencers/{influencer_id}
# -------------------------------------------------
@router.delete("/{influencer_id}")
def delete_influencer(influencer_id: int):
    supabase = get_supabase()

    (
        supabase
        .table("influencers")
        .delete()
        .eq("id", influencer_id)
        .execute()
    )

    return {"status": "deleted"}
