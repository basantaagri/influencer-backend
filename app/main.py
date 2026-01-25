from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ------------------------------------
# ROUTERS (LOCKED)
# ------------------------------------
from app.routes import influencers
from app.routes import audit
from app.routes import saved
from app.routes import reveal
from app.routes import credits
# from app.routes import seed  # ❌ DISABLED IN PRODUCTION

# ------------------------------------
# APP INIT
# ------------------------------------
app = FastAPI(
    title="Influencer Platform Backend",
    version="1.0.0",
)

# ------------------------------------
# CORS (PROD SAFE — FIXED, NO GUESSING)
# ------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # ✅ ACTUAL Cloudflare Pages production URL
        "https://daf8848f.influencer-platform-3u1.pages.dev",

        # ✅ Backend itself (safe, avoids edge cases)
        "https://influencer-backend-supl.onrender.com",

        # ✅ Local dev
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------
# ROUTES
# ------------------------------------

# ✅ Influencers (CORE – PUBLIC)
# 🔒 PREFIX IS DEFINED INSIDE routes/influencers.py
app.include_router(influencers.router)

# ✅ Saved Influencers (JWT PROTECTED)
app.include_router(saved.router)

# ✅ Reveal Influencer (JWT PROTECTED)
app.include_router(reveal.router)

# ✅ Credits (JWT PROTECTED)
app.include_router(credits.router)

# 🔒 Seed DISABLED (SECURITY)
# app.include_router(seed.router)

# ✅ Audit (SAFE / STUBBED)
app.include_router(audit.router)

# ------------------------------------
# HEALTH & AUTH CHECKS
# ------------------------------------
@app.get("/")
def root():
    return {"status": "Backend running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/auth/me")
def auth_me():
    """
    TEMP SAFE STUB
    Frontend expects this endpoint.
    """
    return {
        "id": None,
        "email": None,
        "role": "guest",
    }
