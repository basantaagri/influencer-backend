from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.db import get_supabase
from app.auth import create_access_token, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# -----------------------------
# REQUEST MODELS
# -----------------------------
class RegisterRequest(BaseModel):
    email: str
    password: str
    role: str

class LoginRequest(BaseModel):
    email: str
    password: str

# -----------------------------
# REGISTER
# -----------------------------
@router.post("/register")
def register(data: RegisterRequest):
    supabase = get_supabase()

    # Check if user exists
    existing = (
        supabase
        .table("users")
        .select("id")
        .eq("email", data.email)
        .limit(1)
        .execute()
    )

    if existing.data:
        raise HTTPException(status_code=400, detail="User already exists")

    # Insert user
    response = (
        supabase
        .table("users")
        .insert({
            "email": data.email,
            "password": data.password,  # 🔒 hash later
            "role": data.role
        })
        .execute()
    )

    user = response.data[0]

    token = create_access_token({
        "id": user["id"],
        "email": user["email"],
        "role": user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# -----------------------------
# LOGIN
# -----------------------------
@router.post("/login")
def login(data: LoginRequest):
    supabase = get_supabase()

    response = (
        supabase
        .table("users")
        .select("*")
        .eq("email", data.email)
        .eq("password", data.password)
        .limit(1)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = response.data[0]

    token = create_access_token({
        "id": user["id"],
        "email": user["email"],
        "role": user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# -----------------------------
# CURRENT USER
# -----------------------------
@router.get("/me")
def me(user=Depends(get_current_user)):
    return user
