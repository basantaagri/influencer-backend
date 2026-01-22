from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.auth import get_current_user
from app.db import get_supabase

router = APIRouter(
    prefix="/saved",
    tags=["Saved"]
)

# --------------------------------
# GET ALL SAVED INFLUENCERS (USER-SCOPED)
# --------------------------------
@router.get("/")
def get_saved(user=Depends(get_current_user)):
    supabase = get_supabase()

    response = (
        supabase
        .table("saved_influencers")
        .select("influencer_id, created_at")
        .eq("user_id", user["id"])
        .order("created_at", desc=True)
        .execute()
    )

    return response.data or []

# --------------------------------
# SAVE INFLUENCER (JWT PROTECTED)
# --------------------------------
@router.post("/{influencer_id}")
def save_influencer(
    influencer_id: int,
    user=Depends(get_current_user)
):
    supabase = get_supabase()

    # Prevent duplicates (PER USER)
    exists = (
        supabase
        .table("saved_influencers")
        .select("id")
        .eq("user_id", user["id"])
        .eq("influencer_id", influencer_id)
        .limit(1)
        .execute()
    )

    if exists.data:
        return {"status": "already_saved"}

    supabase.table("saved_influencers").insert({
        "user_id": user["id"],
        "influencer_id": influencer_id,
        "created_at": datetime.utcnow().isoformat()
    }).execute()

    return {"status": "saved"}

# --------------------------------
# REMOVE SAVED INFLUENCER (JWT PROTECTED)
# --------------------------------
@router.delete("/{influencer_id}")
def remove_saved(
    influencer_id: int,
    user=Depends(get_current_user)
):
    response = (
        get_supabase()
        .table("saved_influencers")
        .delete()
        .eq("user_id", user["id"])
        .eq("influencer_id", influencer_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Not found")

    return {"status": "removed"}
