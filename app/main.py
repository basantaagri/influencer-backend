from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# -------------------------------
# ROUTERS
# -------------------------------
from app.routes import influencers, audit, orders, auth, seed

# -------------------------------
# DB INIT
# -------------------------------
from app.init_db import init_db

app = FastAPI(
    title="Influencer Discovery & Audit"
)

# -------------------------------------------------
# CORS (REQUIRED FOR FRONTEND)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# DATABASE LIFECYCLE
# -------------------------------------------------
@app.on_event("startup")
def on_startup():
    init_db()

# -------------------------------------------------
# ROUTES
# -------------------------------------------------

app.include_router(
    influencers.router,
    prefix="/influencers",
    tags=["Influencers"]
)

app.include_router(
    audit.router,
    prefix="/audit",
    tags=["Audit"]
)

app.include_router(
    orders.router,
    prefix="/orders",
    tags=["Orders"]
)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)

# ✅ SEED ROUTE (MANUAL, SAFE)
app.include_router(
    seed.router,
    tags=["Seed"]
)

# -------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------
@app.get("/")
def root():
    return {"status": "Backend running"}
