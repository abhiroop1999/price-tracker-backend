from fastapi import APIRouter
from app.scraper import scrape_product
from app.models import TrackRequest
from app.database import insert_tracking_request

router = APIRouter()

@router.post("/track")
def track_product(data: TrackRequest):
    insert_tracking_request(data)
    return scrape_product(data)
