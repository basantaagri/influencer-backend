from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.db import get_supabase

router = APIRouter()

# -------------------------------------------------
# GET /influencers
# List influencers with optional filters + pagination
# -------------------------------------------------
@router.get("/")
def list_influencers(
    platform: Optional[str] = Query(None),
    niche: Optional[str] = Query(None),
    min_followers: Optional[int] = Query(None, ge=0),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    supabase = get_supabase()

    query = supabase.table("influencers").select("*")

    if platform:
        query = query.eq("platform", platform)

    if niche:
        query = query.eq("niche", niche)

    if min_followers:
        query = query.gte("followers", min_followers)

    res = query.range(offset, offset + limit - 1).execute()

    if res.error:
        raise HTTPException(status_code=400, detail=res.error.message)

    return {
        "count": len(res.data),
        "items": res.data,
        "offset": offset,
        "limit": limit,
    }


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

    if res.error:
        raise HTTPException(status_code=400, detail=res.error.message)

    return {
        "status": "created",
        "data": res.data[0],
    }


# -------------------------------------------------
# GET /influencers/{id}
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

    if res.error:
        raise HTTPException(status_code=404, detail="Influencer not found")

    return res.data


# -------------------------------------------------
# PATCH /influencers/{id}
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

    if res.error:
        raise HTTPException(status_code=400, detail=res.error.message)

    return {
        "status": "updated",
        "updated_rows": len(res.data),
    }


# -------------------------------------------------
# DELETE /influencers/{id}
# -------------------------------------------------
@router.delete("/{influencer_id}")
def delete_influencer(influencer_id: int):
    supabase = get_supabase()

    res = (
        supabase
        .table("influencers")
        .delete()
        .eq("id", influencer_id)
        .execute()
    )

    if res.error:
        raise HTTPException(status_code=400, detail=res.error.message)

    return {"status": "deleted"}
