from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from app.db import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/saved", tags=["Saved"])

# --------------------------------
# GET ALL SAVED INFLUENCERS (USER-SCOPED)
# --------------------------------
@router.get("/")
def get_saved(user_id: str = Depends(get_current_user)):
    conn = get_db()
    rows = conn.execute(
        """
        SELECT influencer_id, created_at
        FROM saved_influencers
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    ).fetchall()
    conn.close()

    return [dict(row) for row in rows]

# --------------------------------
# SAVE INFLUENCER (JWT PROTECTED)
# --------------------------------
@router.post("/{influencer_id}")
def save_influencer(
    influencer_id: int,
    user_id: str = Depends(get_current_user)
):
    conn = get_db()

    # Prevent duplicates (PER USER)
    exists = conn.execute(
        """
        SELECT 1 FROM saved_influencers
        WHERE influencer_id = ? AND user_id = ?
        """,
        (influencer_id, user_id)
    ).fetchone()

    if exists:
        conn.close()
        return {"status": "already_saved"}

    conn.execute(
        """
        INSERT INTO saved_influencers (user_id, influencer_id, created_at)
        VALUES (?, ?, ?)
        """,
        (user_id, influencer_id, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

    return {"status": "saved"}

# --------------------------------
# REMOVE SAVED INFLUENCER (JWT PROTECTED)
# --------------------------------
@router.delete("/{influencer_id}")
def remove_saved(
    influencer_id: int,
    user_id: str = Depends(get_current_user)
):
    conn = get_db()
    cur = conn.execute(
        """
        DELETE FROM saved_influencers
        WHERE influencer_id = ? AND user_id = ?
        """,
        (influencer_id, user_id)
    )
    conn.commit()
    conn.close()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Not found")

    return {"status": "removed"}
