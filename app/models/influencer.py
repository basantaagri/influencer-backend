from pydantic import BaseModel

class Influencer(BaseModel):
    id: int
    name: str
    platform: str
    niche: str
    followers: int
    avg_views: int
    engagement_rate: float
    price: int
    location: str
    language: str
    is_verified: bool
