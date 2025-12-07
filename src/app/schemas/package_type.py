from pydantic import BaseModel, Field


class PackageTypeResponse(BaseModel):
    id: int = Field(..., description="ID типа посылки")
    name: str = Field(..., description="Название типа посылки")

    class Config:
        from_attributes = True  # позволяет строить схему из SQLAlchemy модели
