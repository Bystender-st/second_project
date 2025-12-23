from pydantic import BaseModel
from typing import Optional, Any


class ErrorResponse(BaseModel):
    success: bool = False
    error: str


class SuccessResponse(BaseModel):
    success: bool = True
    data: Optional[Any] = None
