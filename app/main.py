from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# -------------------------------
# ROUTERS (EXISTING)
# -------------------------------
from app.routes import influencers, audit, orders, auth

# -------------------------------
# DB INIT (CRITICAL)
# -------------------------------
from app.init_db import init_db

app = FastAPI(
    title="Influencer Discovery & Audit"
)

# -------------------------------------------------
# CORS (SAFE, REQUIRED FOR FRONTEND)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# DATABASE LIFECYCLE (NON-NEGOTIABLE)
# -------------------------------------------------
@app.on_event("startup")
def on_startup():
    init_db()

# -------------------------------------------------
# ROUTES REGISTRATION (UNCHANGED)
# -------------------------------------------------

# ✅ Influencers
app.include_router(
    influencers.router,
    prefix="/influencers",
    tags=["Influencers"]
)

# ✅ Audit
app.include_router(
    audit.router,
    prefix="/audit",
    tags=["Audit"]
)

# ✅ Orders
app.include_router(
    orders.router,
    prefix="/orders",
    tags=["Orders"]
)

# ✅ Auth
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)

# -------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------
@app.get("/")
def root():
    return {"status": "Backend running"}
