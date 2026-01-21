from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import influencers, seed

app = FastAPI(title="Influencer Discovery & Audit")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(influencers.router, prefix="/influencers", tags=["Influencers"])
app.include_router(seed.router, tags=["Seed"])

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.get("/health")
def health():
    return {"status": "ok"}
