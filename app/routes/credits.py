from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.db import supabase

router = APIRouter(
    prefix="/credits",
    tags=["Credits"]
)

# --------------------------------------------------
# GET USER CREDITS (JWT PROTECTED)
# --------------------------------------------------
@router.get("/")
def get_credits(user_id: str = Depends(get_current_user)):
    result = (
        supabase
        .table("users")
        .select("credits")
        .eq("id", user_id)
        .single()
        .execute()
    )

    # Defensive fallback — never break frontend
    credits = 0
    if result and result.data and "credits" in result.data:
        credits = result.data["credits"]

    return {
        "credits": credits
    }
