from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.db import get_supabase

# -------------------------------------------------
# ROUTER
# -------------------------------------------------
router = APIRouter(
    prefix="/influencers",
    tags=["Influencers"],
)

# -------------------------------------------------
# AUDIENCE SIGNAL (DERIVED — NOT STORED)
# -------------------------------------------------
def get_audience_signal(engagement_rate: Optional[float]):
    if engagement_rate is None:
        return {
            "status": "Needs Review",
            "confidence": "Low",
        }

    if engagement_rate >= 4.0:
        return {
            "status": "Likely Genuine",
            "confidence": "High",
        }

    if engagement_rate >= 2.0:
        return {
            "status": "Likely Genuine",
            "confidence": "Medium",
        }

    if engagement_rate >= 1.0:
        return {
            "status": "Uncertain",
            "confidence": "Low",
        }

    return {
        "status": "Needs Review",
        "confidence": "Low",
    }


# -------------------------------------------------
# GET /influencers
# List influencers with filters + pagination
# RETURNS: always array (frontend safe)
# -------------------------------------------------
@router.get("/")
def list_influencers(
    platform: Optional[str] = Query(None),
    niche: Optional[str] = Query(None),

    # FILTERS (frontend compatible)
    engagement: Optional[str] = Query(None),
    audit: Optional[str] = Query(None),
    price: Optional[str] = Query(None),
    sort: Optional[str] = Query("recommended"),

    # Pagination
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
):
    supabase = get_supabase()
    offset = (page - 1) * per_page

    query = supabase.table("influencers").select("*")

    # -----------------------
    # FILTERS (IGNORE "All")
    # -----------------------
    if platform and platform != "All":
        query = query.eq("platform", platform)

    if niche and niche != "All":
        query = query.eq("niche", niche)

    # Engagement buckets
    if engagement and engagement != "All":
        if engagement == "High":
            query = query.gte("engagement_rate", 4.0)
        elif engagement == "Medium":
            query = query.gte("engagement_rate", 2.5).lt("engagement_rate", 4.0)
        elif engagement == "Low":
            query = query.lt("engagement_rate", 2.5)

    # Audit score filter
    if audit and audit != "All":
        query = query.eq("audit_score", audit)

    # Price buckets
    if price and price != "All":
        if price == "Low":
            query = query.lt("price", 3000)
        elif price == "Medium":
            query = query.gte("price", 3000).lte("price", 6000)
        elif price == "High":
            query = query.gt("price", 6000)

    # -----------------------
    # SORTING
    # -----------------------
    if sort == "Price Low to High":
        query = query.order("price", desc=False)
    elif sort == "Price High to Low":
        query = query.order("price", desc=True)
    elif sort == "Engagement":
        query = query.order("engagement_rate", desc=True)
    else:
        # Recommended (default)
        query = query.order("audit_score", desc=True).order("followers", desc=True)

    res = query.range(offset, offset + per_page - 1).execute()
    data = res.data or []

    # -------------------------------------------------
    # ADD AUDIENCE SIGNAL (SAFE, DERIVED)
    # -------------------------------------------------
    for inf in data:
        inf["audience_signal"] = get_audience_signal(
            inf.get("engagement_rate")
        )

        # classification only (nullable, no inference)
        inf["content_category"] = inf.get("content_category")

    return data


# -------------------------------------------------
# GET /influencers/{id}
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

    data = res.data

    data["audience_signal"] = get_audience_signal(
        data.get("engagement_rate")
    )

    # classification only
    data["content_category"] = data.get("content_category")

    return data


# -------------------------------------------------
# POST /influencers
# Create influencer
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

    # content_category is OPTIONAL (classification only)
    res = supabase.table("influencers").insert(payload).execute()

    return {
        "status": "created",
        "data": res.data[0] if res.data else None,
    }


# -------------------------------------------------
# PATCH /influencers/{id}
# -------------------------------------------------
@router.patch("/{influencer_id}")
def update_influencer(influencer_id: int, payload: dict):
    if not payload:
        raise HTTPException(status_code=400, detail="Empty update payload")

    supabase = get_supabase()

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
# DELETE /influencers/{id}
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
