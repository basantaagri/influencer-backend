from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.db import get_db

router = APIRouter()

# --------------------------------
# GET ALL SAVED INFLUENCERS
# --------------------------------
@router.get("/")
def get_saved():
    conn = get_db()
    rows = conn.execute(
        """
        SELECT influencer_id, created_at
        FROM saved_influencers
        ORDER BY created_at DESC
        """
    ).fetchall()
    conn.close()

    return [dict(row) for row in rows]

# --------------------------------
# SAVE INFLUENCER
# --------------------------------
@router.post("/{influencer_id}")
def save_influencer(influencer_id: int):
    conn = get_db()

    # Prevent duplicates
    exists = conn.execute(
        "SELECT 1 FROM saved_influencers WHERE influencer_id = ?",
        (influencer_id,)
    ).fetchone()

    if exists:
        conn.close()
        return {"status": "already_saved"}

    conn.execute(
        """
        INSERT INTO saved_influencers (influencer_id, created_at)
        VALUES (?, ?)
        """,
        (influencer_id, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

    return {"status": "saved"}

# --------------------------------
# REMOVE SAVED INFLUENCER
# --------------------------------
@router.delete("/{influencer_id}")
def remove_saved(influencer_id: int):
    conn = get_db()
    cur = conn.execute(
        "DELETE FROM saved_influencers WHERE influencer_id = ?",
        (influencer_id,)
    )
    conn.commit()
    conn.close()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Not found")

    return {"status": "removed"}
