from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.db import get_supabase
from app.auth import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# -----------------------------
# GET USER ORDERS
# -----------------------------
@router.get("/")
def get_orders(user=Depends(get_current_user)):
    supabase = get_supabase()

    response = (
        supabase
        .table("orders")
        .select("*")
        .eq("user_id", user["id"])
        .order("created_at", desc=True)
        .execute()
    )

    return response.data or []

# -----------------------------
# CREATE ORDER
# -----------------------------
@router.post("/")
def create_order(
    influencer_id: int,
    user=Depends(get_current_user)
):
    supabase = get_supabase()

    response = (
        supabase
        .table("orders")
        .insert({
            "user_id": user["id"],
            "influencer_id": influencer_id,
            "created_at": datetime.utcnow().isoformat()
        })
        .execute()
    )

    return {"status": "created", "order": response.data[0]}
