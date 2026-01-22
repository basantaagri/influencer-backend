from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user
from app.db import supabase

router = APIRouter(
    prefix="/reveal",
    tags=["Reveal"]
)

# --------------------------------------------------
# REVEAL INFLUENCER (JWT PROTECTED)
# --------------------------------------------------
@router.post("/{influencer_id}")
def reveal_influencer(
    influencer_id: int,
    user_id: str = Depends(get_current_user)
):
    # --------------------------------------------------
    # 1️⃣ Check influencer exists
    # --------------------------------------------------
    influencer_res = (
        supabase
        .table("influencers")
        .select("*")
        .eq("id", influencer_id)
        .single()
        .execute()
    )

    if not influencer_res or not influencer_res.data:
        raise HTTPException(
            status_code=404,
            detail="Influencer not found"
        )

    influencer = influencer_res.data

    # --------------------------------------------------
    # 2️⃣ Check already revealed
    # --------------------------------------------------
    existing = (
        supabase
        .table("influencer_reveals")
        .select("id")
        .eq("user_id", user_id)
        .eq("influencer_id", influencer_id)
        .execute()
    )

    if existing and existing.data:
        return {
            "status": "already_revealed",
            "influencer": influencer
        }

    # --------------------------------------------------
    # 3️⃣ Check user credits
    # --------------------------------------------------
    user_res = (
        supabase
        .table("users")
        .select("credits")
        .eq("id", user_id)
        .single()
        .execute()
    )

    if (
        not user_res
        or not user_res.data
        or user_res.data.get("credits", 0) <= 0
    ):
        raise HTTPException(
            status_code=403,
            detail="Insufficient credits"
        )

    current_credits = user_res.data["credits"]

    # --------------------------------------------------
    # 4️⃣ Deduct one credit
    # --------------------------------------------------
    supabase.table("users").update({
        "credits": current_credits - 1
    }).eq("id", user_id).execute()

    # --------------------------------------------------
    # 5️⃣ Save reveal record
    # --------------------------------------------------
    supabase.table("influencer_reveals").insert({
        "user_id": user_id,
        "influencer_id": influencer_id
    }).execute()

    return {
        "status": "revealed",
        "influencer": influencer
    }
