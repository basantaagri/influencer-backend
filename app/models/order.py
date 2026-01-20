from pydantic import BaseModel

class Order(BaseModel):
    id: int
    influencer_id: int
    brand_name: str
    status: str
