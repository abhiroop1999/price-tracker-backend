from fastapi import APIRouter
from app.scraper import scrape_product
from app.models import TrackRequest
from app.database import insert_tracking_request

router = APIRouter()

@router.post("/track")
def track_product(data: TrackRequest):
    # Step 1: Try scraping
    result = scrape_product(data)

    # Step 2: If there's an error, don't insert anything
    if "error" in result:
        return result

    # Step 3: Only insert valid tracking request into DB
    insert_tracking_request(data)

    return result
