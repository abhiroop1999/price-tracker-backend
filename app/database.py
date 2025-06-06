import os
from sqlalchemy import create_engine, Column, String, Float, Table, MetaData
from app.models import TrackRequest

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
metadata = MetaData()

tracked_items = Table(
    "tracked_items", metadata,
    Column("email", String),
    Column("url", String),
    Column("threshold", Float),
)

metadata.create_all(engine)

def insert_tracking_request(data: TrackRequest):
    with engine.connect() as conn:
        conn.execute(tracked_items.insert().values(
            email=data.email, url=data.url, threshold=data.threshold
        ))
