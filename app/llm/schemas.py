from pydantic import BaseModel
from datetime import date


class AnalyticsRequest(BaseModel):
    metric: str

    creator_id: str | None = None
    target_date: date | None = None
    date_from: date | None = None
    date_to: date | None = None
    views_threshold: int | None = None
