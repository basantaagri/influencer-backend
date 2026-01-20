from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.db import get_db

router = APIRouter()

# --------------------------------
# GET ALL ORDERS
# --------------------------------
@router.get("/")
def get_orders():
    conn = get_db()
    rows = conn.execute(
        """
        SELECT id, influencer_id, influencer_name, price,
               status, created_at
        FROM orders
        ORDER BY created_at DESC
        """
    ).fetchall()
    conn.close()

    return [dict(row) for row in rows]

# --------------------------------
# CREATE ORDER
# --------------------------------
@router.post("/")
def create_order(order: dict):
    required = {"influencer_id", "influencer_name", "price"}
    if not required.issubset(order):
        raise HTTPException(status_code=400, detail="Invalid payload")

    conn = get_db()
    conn.execute(
        """
        INSERT INTO orders
        (influencer_id, influencer_name, price, status, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            order["influencer_id"],
            order["influencer_name"],
            order["price"],
            "pending",
            datetime.utcnow().isoformat()
        )
    )
    conn.commit()
    conn.close()

    return {"status": "created"}

# --------------------------------
# UPDATE ORDER STATUS
# --------------------------------
@router.patch("/{order_id}")
def update_order_status(order_id: int, payload: dict):
    if "status" not in payload:
        raise HTTPException(status_code=400, detail="Missing status")

    conn = get_db()
    cur = conn.execute(
        "UPDATE orders SET status = ? WHERE id = ?",
        (payload["status"], order_id)
    )
    conn.commit()
    conn.close()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"status": "updated"}

# --------------------------------
# DELETE ORDER
# --------------------------------
@router.delete("/{order_id}")
def delete_order(order_id: int):
    conn = get_db()
    cur = conn.execute(
        "DELETE FROM orders WHERE id = ?",
        (order_id,)
    )
    conn.commit()
    conn.close()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"status": "deleted"}
