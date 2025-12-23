from pydantic import BaseModel
from typing import List


class DailyByTypeItem(BaseModel):
    type: str
    count: int
    total_rub: float
    avg_rub: float


class DailyByTypeResponse(BaseModel):
    day: str
    items: List[DailyByTypeItem]
