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
# AUDIENCE SIGNAL (EXISTING — KEEP)
# -------------------------------------------------
def get_audience_signal(engagement_rate: Optional[float]):
    if engagement_rate is None:
        return {"status": "Needs Review", "confidence": "Low"}

    if engagement_rate >= 4.0:
        return {"status": "Likely Genuine", "confidence": "High"}

    if engagement_rate >= 2.0:
        return {"status": "Likely Genuine", "confidence": "Medium"}

    if engagement_rate >= 1.0:
        return {"status": "Uncertain", "confidence": "Low"}

    return {"status": "Needs Review", "confidence": "Low"}


# -------------------------------------------------
# MULTI-SIGNAL AUDIT (DERIVED ONLY)
# -------------------------------------------------
def get_audit_signals(inf: dict):
    followers = inf.get("followers") or 0
    avg_views = inf.get("avg_views") or 0
    engagement_rate = inf.get("engagement_rate")

    # Reach ratio (safe)
    reach_ratio = None
    if followers > 0 and avg_views > 0:
        reach_ratio = round(avg_views / followers, 2)

    # Consistency heuristic
    if engagement_rate is None:
        consistency = "unknown"
    elif engagement_rate >= 2.5:
        consistency = "stable"
    else:
        consistency = "uncertain"

    return {
        "engagement": engagement_rate,
        "reach_ratio": reach_ratio,
        "consistency": consistency,
    }


# -------------------------------------------------
# 🔥 AUDIT SCORE RECOMPOSITION (DERIVED)
# -------------------------------------------------
def recompute_audit_score(base_score: Optional[int], signals: dict):
    if base_score is None:
        return None

    score = base_score

    # Reach efficiency bonus
    rr = signals.get("reach_ratio")
    if rr is not None:
        if rr >= 0.6:
            score += 15
        elif rr >= 0.4:
            score += 10
        elif rr >= 0.2:
            score += 5

    # Consistency penalty
    consistency = signals.get("consistency")
    if consistency == "uncertain":
        score -= 10
    elif consistency == "unknown":
        score -= 5

    return max(0, min(100, score))


# -------------------------------------------------
# ✅ CONFIDENCE TIER (NEW — SAFE, DERIVED)
# -------------------------------------------------
def get_confidence_tier(score: Optional[int]):
    if score is None:
        return "Unknown"
    if score >= 80:
        return "High"
    if score >= 60:
        return "Medium"
    return "Low"


# -------------------------------------------------
# GET /influencers
# -------------------------------------------------
@router.get("/")
def list_influencers(
    platform: Optional[str] = Query(None),
    niche: Optional[str] = Query(None),
    engagement: Optional[str] = Query(None),
    audit: Optional[str] = Query(None),
    price: Optional[str] = Query(None),
    sort: Optional[str] = Query("recommended"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
):
    supabase = get_supabase()
    offset = (page - 1) * per_page

    query = supabase.table("influencers").select("*")

    # -----------------------
    # FILTERS
    # -----------------------
    if platform and platform != "All":
        query = query.eq("platform", platform)

    if niche and niche != "All":
        query = query.eq("niche", niche)

    if engagement and engagement != "All":
        if engagement == "High":
            query = query.gte("engagement_rate", 4.0)
        elif engagement == "Medium":
            query = query.gte("engagement_rate", 2.5).lt("engagement_rate", 4.0)
        elif engagement == "Low":
            query = query.lt("engagement_rate", 2.5)

    if audit and audit != "All":
        if audit == "Good":
            query = query.gte("audit_score_num", 70)
        elif audit == "Medium Risk":
            query = query.gte("audit_score_num", 50).lt("audit_score_num", 70)
        elif audit == "High Risk":
            query = query.lt("audit_score_num", 50)

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
        query = (
            query
            .order("audit_score_num", desc=True)
            .order("engagement_rate", desc=True)
            .order("followers", desc=True)
        )

    res = query.range(offset, offset + per_page - 1).execute()
    data = res.data or []

    # -----------------------
    # DERIVED ENRICHMENT
    # -----------------------
    for inf in data:
        signals = get_audit_signals(inf)
        final_score = recompute_audit_score(
            inf.get("audit_score_num"),
            signals
        )

        inf["audience_signal"] = get_audience_signal(
            inf.get("engagement_rate")
        )
        inf["audit_signals"] = signals
        inf["final_audit_score"] = final_score
        inf["confidence_tier"] = get_confidence_tier(final_score)
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
    signals = get_audit_signals(data)
    final_score = recompute_audit_score(
        data.get("audit_score_num"),
        signals
    )

    data["audience_signal"] = get_audience_signal(
        data.get("engagement_rate")
    )
    data["audit_signals"] = signals
    data["final_audit_score"] = final_score
    data["confidence_tier"] = get_confidence_tier(final_score)
    data["content_category"] = data.get("content_category")

    return data


# -------------------------------------------------
# POST /influencers
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
        "audit_score_num",
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
