from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ------------------------------------
# ROUTERS (LOCKED)
# ------------------------------------
from app.routes import influencers, audit
from app.routes import saved, reveal, credits
# from app.routes import seed  # ❌ DISABLED IN PRODUCTION

# ------------------------------------
# APP INIT
# ------------------------------------
app = FastAPI(
    title="Influencer Platform Backend",
    version="1.0.0"
)

# ------------------------------------
# CORS (SAFE DEFAULT)
# ------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------
# ROUTES
# ------------------------------------

# ✅ Influencers (CORE – PUBLIC)
app.include_router(
    influencers.router,
    prefix="/influencers",
    tags=["Influencers"]
)

# ✅ Saved Influencers (JWT PROTECTED)
app.include_router(
    saved.router
)

# ✅ Reveal Influencer (JWT PROTECTED)
app.include_router(
    reveal.router
)

# ✅ Credits (JWT PROTECTED)
app.include_router(
    credits.router
)

# 🔒 Seed DISABLED (SECURITY)
# app.include_router(
#     seed.router,
#     tags=["Seed"]
# )

# ✅ Audit (SAFE / STUBBED)
app.include_router(
    audit.router
)

# ------------------------------------
# HEALTH & AUTH CHECKS (REQUIRED)
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
    Real JWT logic can be added later.
    """
    return {
        "id": None,
        "email": None,
        "role": "guest"
    }
