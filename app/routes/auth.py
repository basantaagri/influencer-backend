from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from app.db import get_db
from app.utils.auth import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter()


# --------------------------------
# REQUEST SCHEMAS
# --------------------------------
class RegisterBody(BaseModel):
    email: str
    password: str
    role: str  # brand | influencer


class LoginBody(BaseModel):
    email: str
    password: str


# --------------------------------
# REGISTER
# --------------------------------
@router.post("/register")
def register(data: RegisterBody):
    db = get_db()
    cur = db.cursor()

    try:
        cur.execute(
            """
            INSERT INTO users (email, password_hash, role, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                data.email,
                hash_password(data.password),
                data.role,
                datetime.utcnow().isoformat(),
            ),
        )
        db.commit()
    except Exception:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="User exists"
        )

    db.close()
    return {"status": "registered"}


# --------------------------------
# LOGIN (BCRYPT SAFE — FINAL)
# --------------------------------
@router.post("/login")
def login(data: LoginBody):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        """
        SELECT id, password_hash, role
        FROM users
        WHERE email = ?
        """,
        (data.email,),
    )
    user = cur.fetchone()
    db.close()

    # ❌ no plaintext comparison
    if not user or not verify_password(data.password, user[1]):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token({
        "user_id": user[0],
        "role": user[2]
    })

    return {
        "access_token": token,
        "role": user[2],
    }
