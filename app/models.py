from pydantic import BaseModel

class TrackRequest(BaseModel):
    url: str
    threshold: float
    email: str
