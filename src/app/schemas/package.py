from pydantic import BaseModel, Field, field_validator
from typing import Optional

from app.schemas.package_type import PackageTypeResponse


class PackageCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Название посылки")
    weight_kg: float = Field(..., gt=0, description="Вес в килограммах")
    type_id: int = Field(..., description="ID типа посылки")
    content_price_usd: float = Field(
        ..., ge=0, description="Стоимость содержимого в USD"
    )

    @field_validator("weight_kg")
    @classmethod
    def validate_weight(cls, value):
        if value > 10_000:
            raise ValueError("Weight value is unrealistically large")
        return value


class PackageResponse(BaseModel):
    id: int
    name: str
    weight_kg: float
    content_price_usd: float
    delivery_price_rub: Optional[float] = None
    delivery_calculated: bool
    type: PackageTypeResponse

    model_config = {"from_attributes": True}


class PackageListItem(BaseModel):
    id: int
    name: str
    weight_kg: float
    delivery_price_rub: Optional[float]
    delivery_calculated: bool
    type: PackageTypeResponse

    model_config = {"from_attributes": True}


class PackageListResponse(BaseModel):
    items: list[PackageListItem]
    total: int
    page: int
    page_size: int
