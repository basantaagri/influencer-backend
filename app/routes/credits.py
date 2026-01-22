from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user
from app.db import get_supabase

router = APIRouter(
    prefix="/credits",
    tags=["Credits"]
)

# ------------------------------------
# GET USER CREDITS
# ------------------------------------
@router.get("/")
def get_credits(user_id: str = Depends(get_current_user)):
    supabase = get_supabase()

    res = (
        supabase
        .table("users")
        .select("credits")
        .eq("id", user_id)
        .single()
        .execute()
    )

    if not res or not res.data:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "credits": res.data.get("credits", 0)
    }
