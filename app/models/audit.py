from pydantic import BaseModel

class Audit(BaseModel):
    influencer_id: int
    score: int
    label: str
