from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ------------------------------------
# ROUTERS (LOCKED)
# ------------------------------------
from app.routes import seed, influencers

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

# ✅ Influencers (CORE)
app.include_router(
    influencers.router,
    prefix="/influencers",
    tags=["Influencers"]
)

# ✅ Seed (MANUAL / ONE-TIME)
app.include_router(
    seed.router,
    tags=["Seed"]
)

# ------------------------------------
# HEALTH CHECKS
# ------------------------------------
@app.get("/")
def root():
    return {"status": "Backend running"}

@app.get("/health")
def health():
    return {"status": "ok"}
